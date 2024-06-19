from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging
from typing import List
from product_ctx_database_sqlalchemy_14.objects.media_object import MediaDataBase
from product_ctx_database_sqlalchemy_14.objects.media_object import MediaAttributes
from redcircle_integration.external_sources.api_object import ApiSources

@dataclass
class ImageResult:
    link:str
    is_main:bool = False
    
@dataclass
class VideoResult:
    link:str
    type:str


class Media(ABC):
    def __init__(self, api_object=None, **kwargs) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info(f"Media class called")
        self.api_object:ApiSources|None =  api_object
        self.object_database: MediaDataBase = MediaDataBase(log=self.log)

    @abstractmethod
    def update_database(self) -> None:
        pass
    

class MediaRedCircle(Media):
    def __init__(self, ) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info(f"MediaRedCircle class called")
        self.list_media_of_product_attr:List[MediaAttributes] = []
        super().__init__()
        
    def get_list_media_attr_from_images_videos(self,
                                               product_id:int,
                                               images:List[ImageResult],
                                               videos:[VideoResult]) -> List[MediaAttributes]:
        
        self.list_media_of_product_attr.clear()
        
        if images:
            for image in images:
                image:ImageResult
                media_attributes:MediaAttributes = MediaAttributes(product_id=product_id,
                                                                   media_type="Image",
                                                                   name=None,
                                                                   description=None,
                                                                   link_url=image.link,
                                                                   is_main=image.is_main)
                self.list_media_of_product_attr.append(media_attributes)
        
        if videos:
            for video in videos:
                video:VideoResult
                media_attributes:MediaAttributes = MediaAttributes(product_id=product_id,
                                                                   media_type="Video",
                                                                   name=None,
                                                                   description=None,
                                                                   link_url=video.link,
                                                                   is_main=False) 
                self.list_media_of_product_attr.append(media_attributes)
        
        return self.list_media_of_product_attr
        
    def update_database(self, list_media_of_product_attr:MediaAttributes) -> None:
        self.log.info(f"MediaRedCircle save_in_db called")
        for media_attr in list_media_of_product_attr:
            self.object_database.create(media_attr, auto_commit=False)
        self.object_database.save_session_database()
        