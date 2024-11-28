# -*- coding: utf-8 -*-

import json
import os
import pb.datasource_pb2 as datasourcePb
import pb.datasink_pb2 as datasinkPb
import pb.event_pb2 as eventPb
import pb.file_pb2 as filePb
import pb.forward_pb2 as forwardPb

def pbParseThread(pbFileName, pbQue):
    if not pbFileName:
        return
    fileSize = os.path.getsize(pbFileName)
    with open(pbFileName, "rb") as file:
        bFirstFrame = False
        readCount = 0
        while True:
            len_types = file.read(4)
            plugin_value = int.from_bytes(len_types, byteorder='little')
            len_types = file.read(4)
            length = int.from_bytes(len_types, byteorder='little')
            if not length:
                pbQue.put(None)
                break
            pbData = file.read(length)
            readCount = readCount + 4 + length
            progress = int(readCount/fileSize*100)

            pbJson = ""
            match plugin_value:
                case 1:
                    pbJson = parseDatasinkDumpData(pbData, length, progress, bFirstFrame)
                case 2:
                    pbJson = parseDatasourceDumpData(pbData, length, progress, bFirstFrame)
                case 3:
                    pbJson = parseEventDumpData(pbData, length, progress, bFirstFrame)
                case 4:
                    pbJson = parseFileDumpData(pbData, length, progress, bFirstFrame)
                case 5:
                    pbJson = parseForwardDumpData(pbData, length, progress, bFirstFrame)

            if not bFirstFrame:
                bFirstFrame = True

            if pbJson:
                pbQue.put(pbJson)

def parseDatasinkDumpData(pbData, size, progress, bFirstFrame):
    videoFile = f"datasink.ps"
    datasink = datasinkPb.DatasinkDump()
    datasink.ParseFromString(pbData)
    if bFirstFrame:
        with open(videoFile, "wb") as ps:
            ps.write(datasink.datasinkMetaData.frameData)
    else:
        with open(videoFile, "ab") as ps:
            ps.write(datasink.datasinkMetaData.frameData)
    datasinkConfig = {
        "pipelineName": datasink.datasinkConfig.pipelineName
    }
    datasinkMetaData = {
        "index": datasink.datasinkMetaData.frameNo,
        "mediaType": datasink.datasinkMetaData.frameRate,
        "frameType": datasink.datasinkMetaData.mediaType,
        "timestamp": datasink.datasinkMetaData.timeStamp,
        "alarm": datasink.datasinkMetaData.alarm,
        "frameSize": size
    }
    pbJson = {
        "datasinkConfig": datasinkConfig,
        "datasinkMetaData": datasinkMetaData,
        "progress": progress
    }
    return json.dumps(pbJson, ensure_ascii=False, indent=1)

def parseDatasourceDumpData(pbData, size, progress, bFirstFrame):
    videoFile = "datasource.ps"
    datasource = datasourcePb.DatasourceDump()
    datasource.ParseFromString(pbData)
    if not bFirstFrame:
        with open(videoFile, "wb") as ps:
            ps.write(datasource.datasourceStreamInfo.frameData)
    else:
        with open(videoFile, "ab") as ps:
            ps.write(datasource.datasourceStreamInfo.frameData)
    streamConfig = {
        "index": datasource.datasourceStreamConfig.index,
        "timeoutReconnect": datasource.datasourceStreamConfig.timeoutReconnect,
        "streamLoop": datasource.datasourceStreamConfig.streamLoop,
        "imageFlag": datasource.datasourceStreamConfig.imageFlag,
        "url": datasource.datasourceStreamConfig.url,
        "rtspTransport": datasource.datasourceStreamConfig.rtspTransport,
        "uuid": datasource.datasourceStreamConfig.uuid,
        "pipelineName": datasource.datasourceStreamConfig.pipelineName
    }
    streamInfo = {
        "frameNo": datasource.datasourceStreamInfo.frameNo,
        "frameRate": datasource.datasourceStreamInfo.frameRate,
        "mediaType": datasource.datasourceStreamInfo.mediaType,
        "frameType": datasource.datasourceStreamInfo.frameType,
        "timestamp": datasource.datasourceStreamInfo.timeStamp,
        "description": datasource.datasourceStreamInfo.description.decode('utf-8'),
        "frameSize": size
    }
    pbJson = {
        "streamConfig": streamConfig,
        "streamInfo": streamInfo,
        "progress": progress
    }
    return json.dumps(pbJson, ensure_ascii=False, indent=1)

def parseEventDumpData(pbData, size, progress, bFirstFrame):
    event = eventPb.EventDump()
    event.ParseFromString(pbData)
    eventConfig = {
        "extendLibPath": event.eventConfig.extendLibPath,
        "extendLibDesc": event.eventConfig.extendLibDesc,
        "customRule": event.eventConfig.customRule,
        "pipelineName": event.eventConfig.pipelineName
    }
    eventMetaData = {
        "index": event.eventMetaData.index,
        "mediaType": event.eventMetaData.mediaType,
        "frameType": event.eventMetaData.frameType,
        "timestamp": event.eventMetaData.timeStamp,
        "alarm": event.eventMetaData.alarm,
        "uploadAlarmCenter": event.eventMetaData.uploadAlarmCenter,
        "alarmImagePath": event.eventMetaData.alarmImagePath.decode('utf-8'),
        "alarmJsonData": event.eventMetaData.alarmJsonData,
    }
    pbJson = {
        "eventConfig": eventConfig,
        "eventMetaData": eventMetaData,
        "progress": progress
    }
    return json.dumps(pbJson, ensure_ascii=False, indent=1)

def parseFileDumpData(pbData, size, progress, bFirstFrame):
    file = filePb.FileDump()
    file.ParseFromString(pbData)
    fileConfig = {
        "storageDir": file.fileConfig.storageDir,
        "videoFormat": file.fileConfig.videoFormat,
        "videoMaxSize": file.fileConfig.videoMaxSize,
        "videoDuration": file.fileConfig.videoDuration,
        "beforeDuration": file.fileConfig.beforeDuration,
        "afterDuration": file.fileConfig.afterDuration,
        "prefixName": file.fileConfig.prefixName,
        "record": file.fileConfig.record,
        "backgroundImageCapture": file.fileConfig.backgroundImageCapture,
        "pipelineName": file.fileConfig.pipelineName
    }
    fileMetaData = {
        "index": file.fileMetaData.index,
        "mediaType": file.fileMetaData.mediaType,
        "frameType": file.fileMetaData.frameType,
        "timestamp": file.fileMetaData.timeStamp,
        "alarm": file.fileMetaData.alarm,
        "eventId": file.fileMetaData.eventId,
        "analyzeType": file.fileMetaData.analyzeType,
        "record": file.fileMetaData.record
    }
    pbJson = {
        "fileConfig": fileConfig,
        "fileMetaData": fileMetaData,
        "progress": progress
    }
    return json.dumps(pbJson, ensure_ascii=False, indent=1)

def parseForwardDumpData(pbData, size, progress, bFirstFrame):
    videoFile = "forward.ps"
    forward = forwardPb.ForwardDump()
    forward.ParseFromString(pbData)
    if not bFirstFrame:
        with open(videoFile, "wb") as ps:
            ps.write(forward.forwardMetaData.frameData)
    else:
        with open(videoFile, "ab") as ps:
            ps.write(forward.forwardMetaData.frameData)
    forwardConfig = {
        "httpPort": forward.forwardConfig.httpPort,
        "rtspPort": forward.forwardConfig.rtspPort,
        "rtmpPort": forward.forwardConfig.rtmpPort,
        "pipelineName": forward.forwardConfig.pipelineName
    }
    forwardMetaData = {
        "index": forward.forwardMetaData.index,
        "mediaType": forward.forwardMetaData.mediaType,
        "frameType": forward.forwardMetaData.frameType,
        "timestamp": forward.forwardMetaData.timeStamp,
        "errorCode": forward.forwardMetaData.errorCode,
        "frameSize": size
    }
    pbJson = {
        "streamConfig": forwardConfig,
        "streamInfo": forwardMetaData,
        "progress": progress
    }
    return json.dumps(pbJson, ensure_ascii=False, indent=1)