from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Integer, Column, TEXT, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()
metadata = Base.metadata

class Article(Base): 
    __tablename__ = 'article'
    __tableargs__ = (UniqueConstraint('title', 'sub_title', 'text', name='uix_article'),)

    id = Column(Integer, primary_key=True)
    title = Column(TEXT, nullable=False)
    sub_title = Column(TEXT, nullable=False)
    text = Column(TEXT, nullable=False)
    insert_datetime = Column(DateTime(), server_default=func.now())
    def __repr__(self): 
        return f'Article(title={self.title[:50]}, sub_title={self.sub_title[:50]} text={self.text[:50]})'

    def __eq__(self, other): 
        if isinstance(other, Article): 
            return ((self.title == other.title)
                    & (self.sub_title == other.sub_title)
                    & (self.text == other.text))
        return false

class ArticleOccurenceLog(Base):
    __tablename__ = 'article_occurence_log'

    id = Column(Integer, primary_key=True)
    article_id = Column(ForeignKey('article.id'), nullable=False)
    insert_datetime = Column(DateTime(), server_default=func.now(), nullable=False)

    article = relationship(Article)
    
    def __repr__(self): 
        if self.article:
            return f'ArticleOccurenceLog(title={self.article.title[:50]}, article_id={self.article.id}, insert_datetime={self.insert_datetime})\n'
        else:
            return f'ArticleOccurenceLog(article_id={self.article_id}, insert_datetime={self.insert_datetime})\n'

    def __eq__(self, other): 
        if isinstance(other, ArticleOccurenceLog): 
            return ((self.article.id == other.article.id)
                    & (self.insert_datetime == other.insert_datetime))
        return false