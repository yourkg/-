/*
 * Copyright (c) 2020.Huawei Technologies Co., Ltd. All rights reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef POST_PROCESS_H
#define POST_PROCESS_H

#include <queue>
#include "ModuleManager/ModuleManager.h"
#include "ConfigParser/ConfigParser.h"
#include "DvppCommon/DvppCommon.h"
#include "DataType/DataType.h"
#include "Yolov3Post.h"
#include "ModelInfer/ModelInfer.h"

#include<stdio.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<unistd.h>
#include<arpa/inet.h>
#include<string.h>

class PostProcess : public ascendBaseModule::ModuleBase {
public:
    PostProcess();
    ~PostProcess();
    APP_ERROR Init(ConfigParser &configParser, ascendBaseModule::ModuleInitArgs &initArgs);
    APP_ERROR DeInit(void);
    int sockfd;
    struct sockaddr_in addr;
    //int k;
protected:
    APP_ERROR Process(std::shared_ptr<void> inputData);

private:
    APP_ERROR YoloPostProcess(std::vector<RawData> &modelOutput, std::shared_ptr<DeviceStreamData> &dataToSend,
        uint32_t modelType);
    APP_ERROR GetObjectInfoCaffe(std::vector<RawData> &modelOutput, std::vector<ObjDetectInfo> &objInfos);
    APP_ERROR GetObjectInfoTensorflow(std::vector<RawData> &modelOutput, std::vector<ObjDetectInfo> &objInfos);
    void ConstructData(const std::vector<ObjDetectInfo> &objInfos, const std::shared_ptr<DeviceStreamData> &dataToSend)
        const;
    APP_ERROR WriteResult(const std::vector<ObjDetectInfo> &objInfos, uint32_t channelId, uint32_t frameId) const;
    std::string resultPathName_ = {"./result"};
    std::string resultName_ = {};
    std::string resultBakName_ = {};
    uint32_t modelType_ = 0;
    YoloImageInfo yoloImageInfo_ = {};
    std::queue<std::vector<void *>> buffers_ = {};
};

MODULE_REGIST(PostProcess)

#endif
