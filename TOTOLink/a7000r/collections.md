# TOTOLINK A7000R

**固件版本**：9.1.0u.6268_B20220504

|   漏洞编号    |       漏洞文件       |                           漏洞描述                           |            漏洞类型            |
| :-----------: | :------------------: | :----------------------------------------------------------: | :----------------------------: |
| CVE-2024-7213 | /cgi-bin/cstecgi.cgi | setWizardCfg缓冲区溢出<br />sub_428450<br />ssid参数<br />urldecode函数没有限制长度 | 缓冲区溢出（存疑，有长度判断） |
| CVE-2024-7212 | /cgi-bin/cstecgi.cgi | loginAuth函数<br /><br />sub_42D014函数<br />password参数<br />usldecode函数 | 缓冲区溢出（存疑，有长度判断） |
|               |                      |                                                              |                                |
|               |                      |                                                              |                                |

**特殊关注点**：

- [x] url-decode函数
- [x] eval函数
- [x] doSystem函数
- [x] WebsgetVar函数
- [x] Cal_file_md5函数
- [x] getNthValueSafe函数



**固件版本**：V9.1.0u.6115_B20201022

|    漏洞编号     |       漏洞文件       |                        漏洞描述                        |           漏洞类型           |
| :-------------: | :------------------: | :----------------------------------------------------: | :--------------------------: |
| CVE-2023-49418  | /cgi-bin/cstecgi.cgi |                setIpPortFilterRules函数                |          缓冲区溢出          |
| CVE-2023-49417  | /cgi-bin/cstecgi.cgi |   setOpModeCfg函数<br />ssid参数<br />urldecode函数    |          缓冲区溢出          |
| CVE-2023-45985  | /cgi-bin/cstecgi.cgi |   setParentRules函数<br />url参数<br />nvram_set函数   |      缓冲区溢出（存疑）      |
| CVE-2023-36950  | /cgi-bin/cstecgi.cgi |    loginAuth函数<br />http_host参数<br />strcpy函数    |          缓冲区溢出          |
| CNVD-2022-75876 | /cgi-bin/cstecgi.cgi |     addEffect函数<br />sPort参数<br />sprintf函数      |          缓冲区溢出          |
| CVE-2022-37083  | /cgi-bin/cstecgi.cgi |            setDiagnosisCfg函数<br />ip参数             |           命令注入           |
| CVE-2022-37082  | /cgi-bin/cstecgi.cgi |         NTPSyncWithHost函数<br />host_time参数         |           命令注入           |
| CVE-2022-37081  | /cgi-bin/cstecgi.cgi |                  setTracerouteCfg函数                  |           命令注入           |
| CVE-2022-37080  | /cgi-bin/cstecgi.cgi | setTracerouteCfg函数<br />command参数<br />sprintf函数 |          缓冲区溢出          |
| CVE-2022-37079  | /cgi-bin/cstecgi.cgi |           setOpModeCfg函数<br />hostName参数           |           命令注入           |
| CVE-2022-37078  | /cgi-bin/cstecgi.cgi |   setLanguageCfg函数<br />lang参数<br />sprintf函数    |          缓冲区溢出          |
| CVE-2022-37077  | /cgi-bin/cstecgi.cgi |   sub_423970函数<br />pppoeUser参数<br />sprintf函数   |          缓冲区溢出          |
| CVE-2022-37076  | /cgi-bin/cstecgi.cgi |        UploadFirmwareFile函数<br />FileName参数        |           命令注入           |
| CVE-2022-37075  | /cgi-bin/cstecgi.cgi |    setDiagnosisCfg函数<br />ip参数<br />sprintf函数    |          缓冲区溢出          |
| CNVD-2022-50412 | /cgi-bin/cstecgi.cgi |                           无                           | 逻辑缺陷，<br />获取敏感信息 |

