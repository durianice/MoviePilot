from typing import Optional

from pydantic import BaseModel


class MediaServerConf(BaseModel):
    """
    媒体服务器配置
    """
    # 名称
    name: Optional[str] = None
    # 类型 emby/jellyfin/plex
    type: Optional[str] = None
    # 配置
    config: Optional[dict] = {}
    # 是否启用
    enabled: Optional[bool] = False


class DownloaderConf(BaseModel):
    """
    下载器配置
    """
    # 名称
    name: Optional[str] = None
    # 类型 qbittorrent/transmission
    type: Optional[str] = None
    # 是否默认
    default: Optional[bool] = False
    # 配置
    config: Optional[dict] = {}
    # 是否启用
    enabled: Optional[bool] = False


class NotificationConf(BaseModel):
    """
    通知配置
    """
    # 名称
    name: Optional[str] = None
    # 类型 telegram/wechat/vocechat/synologychat
    type: Optional[str] = None
    # 配置
    config: Optional[dict] = {}
    # 场景开关
    switchs: Optional[list] = []
    # 是否启用
    enabled: Optional[bool] = False


class StorageConf(BaseModel):
    """
    存储配置
    """
    # 名称
    name: Optional[str] = None
    # 类型 local/alipan/u115/rclone
    type: Optional[str] = None
    # 配置
    config: Optional[dict] = {}


class TransferDirectoryConf(BaseModel):
    """
    文件整理目录配置
    """
    # 名称
    name: Optional[str] = None
    # 优先级
    priority: Optional[int] = 0
    # 存储
    storage: Optional[str] = None
    # 下载目录
    download_path: Optional[str] = None
    # 适用媒体类型
    media_type: Optional[str] = None
    # 适用媒体类别
    media_category: Optional[str] = None
    # 下载类型子目录
    download_type_folder: Optional[bool] = False
    # 下载类别子目录
    download_category_folder: Optional[bool] = False
    # 监控方式 downloader/monitor，None为不监控
    monitor_type: Optional[str] = None
    # 整理方式 move/copy/link/softlink
    transfer_type: Optional[str] = None
    # 整理到媒体库目录
    library_path: Optional[str] = None
    # 媒体库目录存储
    library_storage: Optional[str] = None
    # 智能重命名
    renaming: Optional[bool] = False
    # 刮削
    scraping: Optional[bool] = False
    # 媒体库类型子目录
    library_type_folder: Optional[bool] = False
    # 媒体库类别子目录
    library_category_folder: Optional[bool] = False
