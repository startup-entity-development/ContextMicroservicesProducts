
from abc import ABC, abstractmethod
from dataclasses import dataclass
from json import dumps
import logging
from typing import List


@dataclass
class Pagination:
    current_page: int
    current_link: str
    total_pages: int
    total_results: int
    next_page: int
    next_page_link: str

    @property
    def json_string(self):
        return dumps({
            "current_page": self.current_page,
            "current_link": self.current_link,
            "total_pages": self.total_pages,
            "total_results": self.total_results,
            "next_page": self.next_page,
            "next_page_link": self.next_page_link
        })
    
    
class PaginationFunctionClass(ABC):
    
    def __init__(self) -> None:
        self.list_of_pagination:List[Pagination] = []
        self.log = logging.getLogger(__name__)
        self.log.info(f"Pagination class called")
        self.initial_pagination:Pagination = None
        self.current_pagination:Pagination = None
        
    def initial_pagination(self,initial_page:Pagination) -> None:
        """Set the initial pagination"""
        self.list_of_pagination.append(initial_page)
        self.initial_pagination = initial_page
        self.current_pagination = initial_page
        self.log.info(f"Initial pagination: {self.current_pagination}")

    def save_list_of_initial_pagination(self, file_name:str="initial_paginations.json"):
        """Save a list of links to be used for pagination"""
        with open(file_name, "w") as file:
                file.truncate(0)
                file.write("[")
                for page in self.list_of_pagination:
                    file.write(page.json_string)
                    if page != self.list_of_pagination[-1]:
                        file.write(",")
                file.write("]")
                
    @abstractmethod
    def get_next_link():
        """Get the next link to be used for pagination"""
        
    @abstractmethod
    def get_prev_link():
        """Get the previous link to be used for pagination"""
        
