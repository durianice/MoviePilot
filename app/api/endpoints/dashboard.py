from pathlib import Path
from typing import Any, List

from fastapi import APIRouter, Depends

from app import schemas
from app.chain.dashboard import DashboardChain
from app.core.config import settings
from app.core.security import verify_token
from app.scheduler import SchedulerChain, Scheduler
from app.utils.string import StringUtils
from app.utils.system import SystemUtils
from app.utils.timer import TimerUtils

router = APIRouter()


@router.get("/statistic", summary="媒体数量统计", response_model=schemas.Statistic)
def statistic(_: schemas.TokenPayload = Depends(verify_token)) -> Any:
    """
    查询媒体数量统计信息
    """
    media_statistic = DashboardChain().media_statistic()
    return schemas.Statistic(
        movie_count=media_statistic.movie_count,
        tv_count=media_statistic.tv_count,
        episode_count=media_statistic.episode_count,
        user_count=media_statistic.user_count
    )


@router.get("/storage", summary="存储空间", response_model=schemas.Storage)
def storage(_: schemas.TokenPayload = Depends(verify_token)) -> Any:
    """
    查询存储空间信息
    """
    if settings.LIBRARY_PATH:
        total_storage, free_storage = SystemUtils.space_usage(Path(settings.LIBRARY_PATH))
    else:
        total_storage, free_storage = 0, 0
    return schemas.Storage(
        total_storage=total_storage,
        used_storage=total_storage - free_storage
    )


@router.get("/processes", summary="进程信息", response_model=List[schemas.ProcessInfo])
def processes(_: schemas.TokenPayload = Depends(verify_token)) -> Any:
    """
    查询进程信息
    """
    return SystemUtils.processes()


@router.get("/downloader", summary="下载器信息", response_model=schemas.DownloaderInfo)
def downloader(_: schemas.TokenPayload = Depends(verify_token)) -> Any:
    """
    查询下载器信息
    """
    transfer_info = DashboardChain().downloader_info()
    free_space = SystemUtils.free_space(Path(settings.DOWNLOAD_PATH))
    return schemas.DownloaderInfo(
        download_speed=transfer_info.download_speed,
        upload_speed=transfer_info.upload_speed,
        download_size=transfer_info.download_size,
        upload_size=transfer_info.upload_size,
        free_space=free_space
    )


@router.get("/schedule", summary="后台服务", response_model=List[schemas.ScheduleInfo])
def schedule(_: schemas.TokenPayload = Depends(verify_token)) -> Any:
    """
    查询后台服务信息
    """
    # 返回计时任务
    schedulers = []
    # 去重
    added = []
    jobs = Scheduler().list()
    # 按照下次运行时间排序
    jobs.sort(key=lambda x: x.next_run_time)
    for job in jobs:
        if job.name not in added:
            added.append(job.name)
        else:
            continue
        if not StringUtils.is_chinese(job.name):
            continue
        next_run = TimerUtils.time_difference(job.next_run_time)
        if not next_run:
            status = "已停止"
        else:
            status = "等待" if job.pending else "运行中"
        schedulers.append(schemas.ScheduleInfo(
            id=job.id,
            name=job.name,
            status=status,
            next_run=next_run
        ))

    return schedulers
