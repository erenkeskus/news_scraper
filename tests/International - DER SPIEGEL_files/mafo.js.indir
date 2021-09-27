!function () {
    let util = {
        // is true -> storage is usable
        _storageStatus: function () {
            let storageTest = function (callback) {
                try {
                    localStorage.getItem('datahub-test') && localStorage.setItem('datahub-test', '1');
                } catch (e) {
                    if (typeof callback !== 'undefined') {
                        callback(false);
                    } else {
                        return false;
                    }
                }
                if (typeof callback !== 'undefined') {
                    callback(true);
                } else {
                    return true;
                }
            };
            if (typeof document.hasStorageAccess === 'function') {
                let promise = document.hasStorageAccess();
                promise.then(
                    function (hasAccess) {
                        this._storageStatus = false;
                        if (hasAccess) {
                            storageTest(function (s) {
                                this._storageStatus = s;
                            }.bind(this))
                        }
                    }.bind(this),
                    function (reason) {
                        this._storageStatus = false;
                    }.bind(this)
                );
                return false;
            } else {
                return storageTest();
            }
        }.call(this),
        _doAjaxRequest: function (settings) {
            var s = window.XDomainRequest ?
                new XDomainRequest() :
                window.XMLHttpRequest ?
                    new XMLHttpRequest() :
                    new ActiveXObject('Microsoft.XMLHTTP');
            var url = settings.url;
            var json = settings.type === 'POST' && settings.useJSON === true;
            s.open(settings.type, url, true);
            if (settings.type === 'POST') {
                if (typeof s.setRequestHeader !== 'undefined') {
                    if (json) {
                        s.setRequestHeader("Content-type", "application/json");
                    } else {
                        s.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    }
                }
                s.send(json ? JSON.stringify(settings.data) : params.join('&'));
            } else {
                s.send(null);
            }
            s.onreadystatechange = function () {
                if (s.status === 200 && s.readyState === 4 && typeof settings.success === 'function') {
                    settings.success(s.responseText);
                } else if (s.readyState === 4 && s.status !== 200 && typeof settings.failed === 'function') {
                    settings.failed();
                }
            };
        }
    };

    var mafo = function () {
        this._dateStorageName = "_lastRequested";
        this._adCallDataName = "_adCallData";
        if (util._storageStatus) {
            if (!localStorage.getItem(this._adCallDataName)) {
                localStorage.setItem(this._adCallDataName, JSON.stringify({client: {}, server: {}}));
            }
        }
        this.lastRequested = function () {
            if (util._storageStatus) {
                var value = localStorage.getItem(this._dateStorageName);
                if (value !== null && value !== "") {
                    return parseInt(value);
                }
                return 0;
            } else {
                return new Date().getTime();
            }
        }.call(this);
        this.mafoClientDataExists = function() {
            var exists = false;
            var clientData = this._getAdCallData().client;
            if(Object.keys(clientData).length > 0) {
                exists = true;
            }
            return exists;
        };
        if ((this.lastRequested + 12 * 60 * 60 * 1000) < (new Date().getTime()) && this.mafoClientDataExists()) {
            /****
             * Request to Server for Validation
             ****/
            localStorage.setItem(this._dateStorageName, new Date().getTime() + '');
            this._sendClientData();
        }
    };
    mafo.prototype = {
        listen: function () {
            window.addEventListener('message', function (event) {
                if (!util._storageStatus) {
                    return;
                }
                var elementData;
                var data;
                if (typeof event.data !== 'undefined' && typeof event.data.indexOf === 'function') {
                    if (event.data.indexOf('GujAd:mafo::SubmitElement:') === 0) {
                        elementData = JSON.parse(event.data.replace('GujAd:mafo::SubmitElement:', ''));
                        /****
                         * save to storage
                         * Submit Data for Storage
                         * elementData.orderId
                         * elementData.creativeId
                         * elementData.lineitemId
                         * elementData.adUnit
                         ****/
                        this._saveClientDataToStorage(elementData.orderId, elementData.creativeId, elementData.lineitemId, elementData.adUnit);
                    } else if (event.data.indexOf('GujAd:mafo::GetDataForLink:') === 0) {
                        elementData = JSON.parse(event.data.replace('GujAd:mafo::GetDataForLink:', ''));
                        /****
                         * Send Data for Link generating to Client
                         * elementData.orderId
                         ****/
                        data = this._getOrderData(elementData.orderId);
                        // sending
                        event.source.postMessage('GujAd:mafo::SendDataForLink::' + JSON.stringify(data), '*');
                    } else if (event.data.indexOf('GujAd:mafo::GetDataForAdCall') === 0) {
                        /****
                         * all orderids that can have a layer
                         * Send OrderIds for AdCall
                         ****/
                        data = this._getLayerOrderIdsFromStorage();
                        // sending
                        event.source.postMessage('GujAd:mafo::SendDataForAdCall::' + JSON.stringify(data), '*');
                    } else if (event.data.indexOf('GujAd:mafo::SubmitFinish') === 0) {
                        // layer for order succesfully delivered to client. set all entries of that order in localstorage to finished
                        var orderId = event.data.replace('GujAd:mafo::SubmitFinish:', '');
                        this._setOrderToFinished(orderId);
                    }
                }
            }.bind(this));
        },
        _saveClientDataToStorage: function (orderId, creativeId, lineItemId, adUnit) {
            var dataParsed = this._getAdCallData();
            var key = orderId + ':' + creativeId + ':' + lineItemId + ':' + adUnit;
            if (dataParsed.client.hasOwnProperty(key)) {
                dataParsed.client[key].count += 1;
            } else {
                dataParsed.client[key] = {
                    firstImpressionTime: new Date().getTime(),
                    lastUpdateTime: null,
                    count: 1,
                    finished: false
                }
            }
            localStorage.setItem(this._adCallDataName, JSON.stringify(dataParsed));
        },
        _getAdCallData: function () {
            return JSON.parse(localStorage.getItem(this._adCallDataName));
        },
        _sendClientData: function () {
            util._doAjaxRequest({
                type: 'POST',
                url: 'https://mafo.adalliance.io/service/orders/showlayer',
                useJSON: true,
                data: this._getAdCallData().client,
                success: function (res) {
                    this._saveServerDataToStorage(res);
                }.bind(this),
                failed: function () {
                    console.log('failed');
                }
            })
        },
        _saveServerDataToStorage: function (response) {
            var dataParsed = this._getAdCallData();
            var data = JSON.parse(response);
            data.forEach(function (entry) {
                for (var key in entry) {
                    if (entry.hasOwnProperty(key)) {
                        dataParsed.server[key] = entry[key];
                    }
                }
            });
            localStorage.setItem(this._adCallDataName, JSON.stringify(dataParsed));
        },
        _getLayerOrderIdsFromStorage: function () {
            var orderIds = [];
            var adCallData = localStorage.getItem(this._adCallDataName);
            var dataParsed = JSON.parse(adCallData);
            for (var key in dataParsed.server) {
                if (dataParsed.server.hasOwnProperty(key)) {
                    if (!dataParsed.server[key].finished) {
                        orderIds.push(key.split(':')[0]);
                    }
                }
            }
            return orderIds;
        },
        _setOrderToFinished: function (orderId) {
            var dataParsed = this._getAdCallData();
            for (var key in dataParsed.server) {
                if (dataParsed.server.hasOwnProperty(key)) {
                    var splitted = key.split(':');
                    var parsedOrderId = splitted[0];
                    if (parsedOrderId === orderId) {
                        dataParsed.server[key].finished = true;
                    }
                }
            }
            localStorage.setItem(this._adCallDataName, JSON.stringify(dataParsed));
        },
        _getOrderData: function (orderId) {
            var results = [];
            var dataParsed = this._getAdCallData();
            for (var key in dataParsed.server) {
                if (dataParsed.server.hasOwnProperty(key)) {
                    var value = dataParsed.server[key];
                    var splitted = key.split(':');
                    var parsedOrderId = splitted[0];
                    if (parsedOrderId === orderId && !value.finished) {
                        var creativeId = splitted[1];
                        var lineItemId = splitted[2];
                        var adUnitId = splitted[3];
                        results.push({
                            orderId: parsedOrderId,
                            creativeId: creativeId,
                            lineItemId: lineItemId,
                            adUnitId: adUnitId,
                            count: value.count,
                            firstImpressionTime: value.firstImpressionTime
                        })
                    }
                }
            }
            return results;
        }
    };

    if (location.href.indexOf('cookie_consent=0') === -1) {
        let instance = new mafo();
        instance.listen();
    }
}();
