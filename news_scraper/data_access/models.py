from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Integer, Column, TEXT, DateTime, ForeignKey
from sqlalchemy.sql import func

Base = declarative_base()
metadata = Base.metadata

class Article(Base): 
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(TEXT(convert_unicode=True))
    sub_title = Column(TEXT(convert_unicode=True))
    text = Column(TEXT(convert_unicode=True))
    insert_datetime = Column(DateTime(), server_default=func.now())
    def __repr__(self): 
        return f'Article(title={self.title}, \nsub_title={self.sub_title} \
            \ntext={self.text[:50]}'

    def __eq__(self, other): 
        if isinstance(other, Article): 
            return ((self.title == other.title)
                    & (self.sub_title == other.sub_title)
                    & (self.text == other.text))
        return false

class ArticleOccurenceLog(Base):
    __tablename__ = 'article_occurence_log'

    id = Column(Integer, primary_key=True)
    article_id = Column(ForeignKey('article.id'))
    datetime = Column(DateTime(), server_default=func.now())


