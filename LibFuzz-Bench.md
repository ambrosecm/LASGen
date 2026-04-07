# **LibFuzz-Bench**

## **libtiff** ( 3 : 2 from existing datasets + 1 newly added )

[Source code](https://gitlab.com/libtiff/libtiff)

* 4.0.9

|**CVE**|**Function**|**Version**|
|-|-|-|
|CVE-2018-7456|TIFFPrintDirectory|4.0.9|
|CVE-2017-18013|TIFFPrintDirectory|4.0.9|

AFGEN

* 4.4.0

|**CVE**|**Function**|**Version**|
|-|-|-|
|CVE-2022-34526|\_TIFFVGetField|4.4.0|

## **ngiflib** ( 13 : 9 from existing datasets + 4 newly added )

[Source Code](https://github.com/miniupnp/ngiflib)

* 3bb9980
* b588a22
* 75b9920

|**CVE**|**Function**|**Version**|
|-|-|-|
|CVE-2018-10677|WritePixels|75b9920|
|CVE-2018-10717|WritePixels|b588a22|
|CVE-2018-11575|DecodeGifImg|b588a22|
|CVE-2018-11576|GifIndexToTrueColor|b588a22|
|CVE-2018-11578|GifIndexToTrueColor|b588a22|
|CVE-2019-16346|WritePixel|b588a22|
|CVE-2019-16347|WritePixels|3bb9980|
|CVE-2019-19011|GifIndexToTrueColor|3bb9980|
|CVE-2019-20219|GifIndexToTrueColor|3bb9980|

AFGEN

* 0245fd4

|**CVE**|**Function**|**Version**|
|-|-|-|
|CVE-2021-36530|GetByteStr|0245fd4|
|CVE-2021-36531|GetByte|0245fd4|
|CVE-2022-30857|SDL\_LoadAnimatedGif|0245fd4|
|**CVE-2022-30858**|SDL\_LoadAnimatedGif|0245fd4|

## **libwav** ( 8 : 7 from existing datasets + 1 newly added)

[Source Code](https://github.com/marc-q/libwav)

* 5cc8746

|**CVE**|**Func**|**Ver**|
|-|-|-|
|CVE-2018-14049|print\_info|5cc8746|
|CVE-2018-14050|wav\_free-gain\_file|5cc8746|
|CVE-2018-14051|wav\_read|5cc8746|
|CVE-2018-14052|apply\_gain|5cc8746|
|CVE-2018-14549|wav\_write|5cc8746|
|CVE-2019-16348|gain\_file|5cc8746|
|CVE-2019-19698|wav\_content\_read|5cc8746|

AFGEN

* 5cc8746

|**CVE**|**Function**|**Version**|
|-|-|-|
|CVE-2020-28176|wav\_gain|5cc8746|

## **ffjpeg** ( 13 : 12 from existing datasets + 1 newly added )

[Source Code](https://github.com/rockcarry/ffjpeg)

* 627c8a9
* d615881

|**CVE**|**Func**|**Ver**|
|-|-|-|
|CVE-2019-16350|idct2d8x8|627c8a9|
|CVE-2019-16351|huffman\_decode\_step|627c8a9|
|CVE-2019-16352|jfif\_load|627c8a9|
|CVE-2019-19887|bitstr\_tell|627c8a9|
|CVE-2019-19888|jfif\_decode|627c8a9|
|CVE-2020-13438|jfif\_encode|627c8a9|
|CVE-2020-13439|jfif\_decode|627c8a9|
|CVE-2020-13440|bmp\_load|627c8a9|
|CVE-2020-15470|jfif\_decode|d615881|
|CVE-2020-23705|jfif\_encode|627c8a9|
|CVE-2020-23851|jfif\_decode|d615881|
|CVE-2020-23852|jfif\_decode|627c8a9|

AFGEN

* **d5cfd49**

|**CVE**|**Function**|**Version**|
|-|-|-|
|CVE-2021-45385|**bmp\_load**|**d5cfd49**|

## **tcpreplay** ( 26 : 16 from existing datasets + 10 newly added )

[Source Code](https://github.com/appneta/tcpreplay)

* 4.2.6
* 4.3.0
* 4.3.1
* 4.3.3

|**CVE**|**Func**|**Ver**|
|-|-|-|
|CVE-2018-13112|get\_l2len|4.2.6|
|CVE-2018-17580|fast\_edit\_packet|4.2.6|
|CVE-2018-17582|get\_next\_packet|4.2.6|
|CVE-2018-17974|dlt\_en10mb\_encode|4.2.6|
|CVE-2018-18407|csum\_replace4|4.2.6|
|CVE-2018-18408|post\_args()|4.2.6|
|CVE-2018-20552|packet2tree|4.3.0|
|CVE-2018-20553|get\_l2len|4.3.0|
|CVE-2019-8376|get\_layer4\_v6|4.3.1|
|CVE-2019-8377|get\_ipv6\_l4proto|4.3.1|
|CVE-2019-8381|do\_checksum|4.3.1|
|CVE-2020-12740|get\_ipv6\_next|4.3.1|
|CVE-2020-18976|do\_checksum|4.3.1|
|CVE-2020-23273|randomize\_iparp|4.3.1|
|CVE-2020-24265|get\_l2len|4.3.3|
|CVE-2020-24266|get\_l2len|4.3.3|

AFGEN

* 4.3.4
* 4.4.1
* 4.4.3

|**CVE**|**Function**|**Version**|
|-|-|-|
|CVE-2021-45386|add\_tree\_ipv6|4.3.4|
|CVE-2021-45387|add\_tree\_ipv4|4.3.4|
|CVE-2022-25484|packet2tree|4.4.1|
|CVE-2023-27783|tcpedit\_dlt\_cleanup|4.4.3|
|CVE-2023-27784|**read\_hexstring**|4.4.3|
|CVE-2023-27785|**parse\_endpoints**|4.4.3|
|CVE-2023-27786|**macinstring**|4.4.3|
|CVE-2023-27787|**parse\_list**|4.4.3|
|CVE-2023-27788|**ports2PORT**|4.4.3|
|CVE-2023-27789|**cidr2cidr**|4.4.3|

## **jasper** ( 8 from existing datasets )

[Source Code](https://github.com/jasper-software/jasper)

* 2.0.14

|**CVE**|**Func**|**Ver**|
|-|-|-|
|CVE-2018-18873|ras\_putdatastd|2.0.14|
|CVE-2018-19139|jpc\_unk\_getparms|2.0.14|
|CVE-2018-19539|jas\_image\_readcmpt|2.0.14|
|CVE-2018-19540|jas\_icctxtdesc\_input|2.0.14|
|CVE-2018-20570|jp2\_encode|2.0.14|
|CVE-2018-9055|jpc\_firstone|2.0.14|
|CVE-2018-9154|jpc\_dec\_process\_sot|2.0.14|
|CVE-2018-9252|jpc\_abstorelstepsize|2.0.14|

## **jhead** ( 10: 9 from existing datasets + 1 newly added )

[Source Code](https://github.com/Matthias-Wandel/jhead)

* 3.00
* 3.03
* 3.04

|**CVE**|**Func**|**Ver**|
|-|-|-|
|CVE-2018-16554|ProcessGpsInfo|3.00|
|CVE-2018-17088|ProcessExifDir|3.00|
|CVE-2018-6612|process\_EXIF|3.00|
|CVE-2019-1010301|ProcessGpsInfo|3.03|
|CVE-2019-1010302|show\_IPTC|3.03|
|CVE-2019-19035|ReadJpegSections|3.03|
|CVE-2020-6624|process\_DQT|3.04|
|CVE-2020-6625|ProcessGpsInfo|3.04|
|CVE-2021-3496|Get16u|3.06（**871e319**）|

AFGEN

* 3.06

|**CVE**|**Function**|**Version**|
|-|-|-|
|CVE-2022-28550|shellescape|3.06|

## **Oniguruma** ( 1 from existing datasets )

[Source Code](https://github.com/kkos/oniguruma)

* 6.9.3

|**CVE**|**Func**|**Ver**|
|-|-|-|
|CVE-2019-19203|gb18030\_mbc\_enc\_len|6.9.3|

## **lupng** ( 3 from existing datasets )

[Source Code](https://github.com/jansol/LuPng)

* d8f695c

|**CVE**|**Func**|**Ver**|
|-|-|-|
|CVE-2018-18581|internalPrintf|d8f695c|
|CVE-2018-18582|insertByte|d8f695c|
|CVE-2018-18583|insertByte|d8f695c|

## **libming** ( 29 : 25 from existing datasets + 4 newly added )

[Source Code](https://github.com/libming/libming)

* 0.4.8

|**CVE**|**Func**|**Ver**|
|-|-|-|
|CVE-2018-11100|decompileSETTARGET|0.4.8|
|CVE-2018-20428|strlenext|0.4.8|
|CVE-2018-7873|getString|0.4.8|
|CVE-2018-7874|strlenext|0.4.8|
|CVE-2018-7877|getString|0.4.8|
|CVE-2019-16705|OpCode|0.4.8|
|CVE-2020-6629|decompileGETURL2|0.4.8|
|CVE-2017-11732|dcputs|0.4.8|
|CVE-2017-11733|stackswap|0.4.8|
|CVE-2017-11734|decompileCALLFUNCTION|0.4.8|
|CVE-2017-16883|outputSWF\_TEXT\_RECORD|0.4.8|
|CVE-2018-11017|decompileCALLMETHOD|0.4.8|
|CVE-2018-11095|decompileJUMP|0.4.8|
|CVE-2018-20591|decompileJUMP|0.4.8|
|CVE-2018-6315|outputSWF\_TEXT\_RECORD|0.4.8|
|CVE-2018-7867|getString|0.4.8|
|CVE-2018-7868|getName|0.4.8|
|CVE-2018-7870|getString|0.4.8|
|CVE-2018-7871|getName|0.4.8|
|CVE-2018-7875|getString|0.4.8|
|CVE-2021-34342|decompileNEWOBJECT|0.4.8|
|CVE-2018-7872|getName|0.4.8|
|CVE-2018-9165|getName|0.4.8|
|CVE-2018-11226|getString|0.4.8|
|CVE-2019-9113|getString|0.4.8|

AFGEN

* 04aee52

|**CVE**|**Function**|**Version**|
|-|-|-|
|CVE-2023-23052|makeswf|04aee52|
|CVE-2023-23053|makeswf|04aee52|
|CVE-2023-23054|SWFShape\_drawCubic|04aee52|
|CVE-2023-23051|makeswf|04aee52|

## **liblouis** ( 13 : 10 from existing datasets + 3 newly added )

[Source Code](https://github.com/liblouis/liblouis)

* 3.2.0
* 3.5.0
* 3.6.0

|**CVE**|**Func**|**Ver**|
|-|-|-|
|CVE-2018-17294|matchCurrentInput|3.6.0|
|CVE-2017-13743|\_lou\_showString|3.2.0|
|CVE-2017-13742|includeFile|3.2.0|
|CVE-2017-13741|compileBrailleIndicator|3.2.0|
|CVE-2017-13740|parseChars|3.2.0|
|CVE-2017-13739|resolveSubtable|3.2.0|
|CVE-2017-13738|\_lou\_getALine|3.2.0|
|CVE-2018-11440|parseChars|3.5.0|
|CVE-2018-11577|lou\_logPrint|3.5.0|
|CVE-2018-11685|compileHyphenation|3.5.0|

AFGEN

* 3.24.0（6223f21）

|**CVE**|**Function**|**Version**|
|-|-|-|
|CVE-2023-26767|**lou\_setDataPath**|3.24.0（6223f21）|
|CVE-2023-26768|**lou\_logFile**|3.24.0（6223f21）|
|CVE-2023-26769|resolveSubtable|3.24.0（6223f21）|

# total table

||**CVE（127）**|**Function**|**Version**|
|-|-|-|-|
|**libtiff 3=2+1**|CVE-2018-7456|TIFFPrintDirectory|4.0.9|
||CVE-2017-18013|TIFFPrintDirectory|4.0.9|
||**CVE-2022-34526**|**tiffcp → TIFFGetField → TIFFVGetField → \_TIFFVGetField**|**4.4.0**|
|**ngiflib 13=9+4**|CVE-2018-10677|WritePixels|75b9920|
||CVE-2018-10717|WritePixels|b588a22|
||CVE-2018-11575|LoadGif → DecodeGifImg|b588a22|
||CVE-2018-11576|GifIndexToTrueColor|b588a22|
||CVE-2018-11578|GifIndexToTrueColor|b588a22|
||CVE-2019-16346|WritePixel|b588a22|
||CVE-2019-16347|WritePixels|3bb9980|
||CVE-2019-19011|GifIndexToTrueColor|3bb9980|
||CVE-2019-20219|GifIndexToTrueColor|3bb9980|
||**CVE-2021-36530**|**GetByteStr**|**0245fd4**|
||**CVE-2021-36531**|**GetByte**|**0245fd4**|
||**CVE-2022-30857**|**SDL\_LoadAnimatedGif**|**0245fd4**|
||**CVE-2022-30858**|**SDL\_LoadAnimatedGif**|**0245fd4**|
|**libwav 8=7+1**|CVE-2018-14049|print\_info|5cc8746|
||CVE-2018-14050|gain\_file → wav\_free|5cc8746|
||CVE-2018-14051|gain\_file → wav\_read|5cc8746|
||CVE-2018-14052|apply\_gain|5cc8746|
||CVE-2018-14549|gain\_file → wav\_write|5cc8746|
||CVE-2019-16348|gain\_file|5cc8746|
||CVE-2019-19698|wav\_content\_read|5cc8746|
||**CVE-2020-28176**|**wav\_gain — wav\_chunk\_read**|**5cc8746**|
|**ffjpeg 13=12+1**|CVE-2019-16350|jfif\_decode → idct2d8x8|627c8a9|
||CVE-2019-16351|jfif\_decode → huffman\_decode\_step|627c8a9|
||CVE-2019-16352|jfif\_load|627c8a9|
||CVE-2019-19887|jfif\_encode → bitstr\_tell|627c8a9|
||CVE-2019-19888 (Arithmetic exception)|jfif\_decode|627c8a9|
||CVE-2020-13438 (Segmentation fault)|jfif\_encode|627c8a9|
||CVE-2020-13439 (Segmentation fault)|jfif\_decode|627c8a9|
||CVE-2020-13440|bmp\_load|627c8a9|
||CVE-2020-23852 (heap-overflow)|jfif\_decode|627c8a9|
||CVE-2020-23705|jfif\_encode|627c8a9|
||CVE-2020-23851 (stack-buffer-overflow)|jfif\_decode|d615881|
||CVE-2020-15470 (heap-overflow)|jfif\_decode|d615881|
||**CVE-2021-45385**|\*\*bmp\_load、\*\***jfif\_encode**|**d5cfd49**|
|**tcpreplay 26=16+10**|CVE-2018-13112|process\_raw\_packets → get\_ipv4 → get\_l2len|4.2.6|
||CVE-2018-17580|tcpreplay\_replay → tcpr\_replay\_index → replay\_file → send\_packets → fast\_edit\_packet|4.2.6|
||CVE-2018-17582|preload\_pcap\_file → get\_next\_packet|4.2.6|
||CVE-2018-17974|tcpreplay\_replay → tcpr\_replay\_index → replay\_file → send\_packets → tcpedit\_packet → tcpedit\_dlt\_process → tcpedit\_dlt\_encode → dlt\_en10mb\_encode|4.2.6|
||CVE-2018-18407|tcpreplay\_replay → tcpr\_replay\_index → replay\_file → send\_packets → tcpedit\_packet → randomize\_ipv4 → ipv4\_l34\_csum\_replace → ipv4\_addr\_csum\_replace → csum\_replace4|4.2.6|
||CVE-2018-18408|post\_args|4.2.6|
||CVE-2018-20552|process\_raw\_packets → add\_tree\_ipv4 → packet2tree|4.3.0|
||CVE-2018-20553|process\_raw\_packets → get\_ipv4 → get\_l2len|4.3.0|
||CVE-2019-8376|tcpreplay\_replay → tcpr\_replay\_index → replay\_file → send\_packets → tcpedit\_packet → fix\_ipv4\_checksums → do\_checksum → get\_layer4\_v6|4.3.1|
||CVE-2019-8377|tcpreplay\_replay → tcpr\_replay\_index → replay\_file → send\_packets → tcpedit\_packet → fix\_ipv4\_checksums → do\_checksum → get\_ipv6\_l4proto|4.3.1|
||CVE-2019-8381|tcpreplay\_replay → tcpr\_replay\_index → replay\_file → send\_packets → tcpedit\_packet → fix\_ipv4\_checksums → do\_checksum|4.3.1|
||CVE-2020-12740|rewrite\_packets → tcpedit\_packet → fix\_ipv4\_checksums → do\_checksum → get\_ipv6\_l4proto → get\_ipv6\_l4proto → get\_ipv6\_next|4.3.1|
||CVE-2020-18976|tcpreplay\_replay → tcpr\_replay\_index → replay\_file → send\_packets → tcpedit\_packet → fix\_ipv4\_checksums → do\_checksum|4.3.1|
||CVE-2020-23273|tcpreplay\_replay → tcpr\_replay\_index → replay\_file → send\_packets → tcpedit\_packet → randomize\_iparp|4.3.1|
||CVE-2020-24265|process\_raw\_packets → get\_ipv4 → get\_l2len|4.3.3|
||CVE-2020-24266|process\_raw\_packets → get\_ipv4 → get\_l2len|4.3.3|
||**CVE-2021-45386**|**process\_raw\_packets → add\_tree\_ipv6**|**4.3.4**|
||**CVE-2021-45387**|**process\_raw\_packets → add\_tree\_ipv4**|**4.3.4**|
||**CVE-2022-25484**|**process\_raw\_packets → add\_tree\_ipv4 → packet2tree**|**4.4.1**|
||**CVE-2023-27783**|**tcpedit\_close → dlt\_jnpr\_ether\_cleanup → tcpedit\_dlt\_cleanup**|**4.4.3**|
||**CVE-2023-27784**|**tcpedit\_post\_args → tcpedit\_dlt\_post\_args → tcpedit\_dlt\_parse\_opts → dlt\_user\_parse\_opts → read\_hexstring**|**4.4.3**|
||**CVE-2023-27785**|**tcpedit\_post\_args → parse\_endpoints**|**4.4.3**|
||**CVE-2023-27786**|**process\_raw\_packets → macinstring**|**4.4.3**|
||**CVE-2023-27787**|**optionProcess → doOptInclude → parse\_xX\_str → parse\_list**|**4.4.3**|
||**CVE-2023-27788**|**tcpedit\_post\_args → parse\_portmap → ports2PORT**|**4.4.3**|
||**CVE-2023-27789**|**optionProcess → doOptCidr → parse\_cidr → cidr2cidr**|**4.4.3**|
|**jasper 8**|CVE-2018-18873|ras\_encode → ras\_putdatastd|2.0.14|
||CVE-2018-19139|jas\_image\_decode → jpc\_decode → jpc\_dec\_decode → jpc\_getms → jpc\_unk\_getparms jas\_image\_decode →  jpc\_decode → jpc\_dec\_decode → jpc\_dec\_process\_sot|2.0.14|
||CVE-2018-19539|jas\_image\_encode → bmp\_encode → bmp\_putdata → jas\_image\_readcmpt|2.0.14|
||CVE-2018-19540|jas\_image\_decode → jp2\_decode → jas\_iccprof\_load → jas\_icctxtdesc\_input|2.0.14|
||CVE-2018-20570|jas\_image\_encode → jp2\_encode|2.0.14|
||CVE-2018-9055|jas\_image\_encode → jpc\_encode → jpc\_firstone|2.0.14|
||CVE-2018-9154|jas\_image\_decode →  jpc\_decode → jpc\_dec\_decode → jpc\_dec\_process\_sot|2.0.14|
||CVE-2018-9252|jas\_image\_encode → jp2\_encode → jpc\_encode → jpc\_enc\_encodemainhdr → jpc\_abstorelstepsize|2.0.14|
|**jhead 10=9+1**|CVE-2018-16554|ProcessFile → ReadJpegFile → ReadJpegSections → process\_EXIF → ProcessExifDir → ProcessGpsInfo|3.00|
||CVE-2018-17088|ProcessFile → ReadJpegFile → ReadJpegSections → process\_EXIF → ProcessExifDir|3.00|
||CVE-2018-6612|ProcessFile → ReadJpegFile → ReadJpegSections → process\_EXIF|3.00|
||CVE-2019-1010301|ProcessFile → ReadJpegFile → ReadJpegSections → process\_EXIF → ProcessExifDir → ProcessGpsInfo|3.03|
||CVE-2019-1010302|ProcessFile → show\_IPTC|3.03|
||CVE-2019-19035|ProcessFile → ReadJpegFile → ReadJpegSections|3.03|
||CVE-2020-6624|ProcessFile → ReadJpegFile → ReadJpegSections → process\_DQT|3.04|
||CVE-2020-6625|ProcessFile → ReadJpegFile → ReadJpegSections → process\_EXIF → ProcessExifDir → ProcessGpsInfo|3.04|
||CVE-2021-3496|ProcessFile → ReadJpegFile → ReadJpegSections → process\_EXIF → ProcessExifDir → ProcessMakerNote → ProcessCanonMakerNoteDir → Get16u|3.06 ( **871e319)**|
||**CVE-2022-28550**|**ProcessFile → DoCommand → shellescape**|**3.06**|
|**Oniguruma 1**|CVE-2019-19203|onig\_search → search\_in\_range → gb18030\_mbc\_to\_code → onigenc\_mbn\_mbc\_to\_code → gb18030\_mbc\_enc\_len|6.9.3|
|**lupng 3**|CVE-2018-18581|luPngReadFile → luPngReadUC → readChunk → internalPrintf|d8f695c|
||CVE-2018-18582|luPngReadFile → luPngReadUC → insertByte|d8f695c|
||CVE-2018-18583|luPngReadFile → luPngReadUC → handleChunk → parseIdat → insertByte|d8f695c|
|**libming  29=25+4**|CVE-2018-11100|main → readMovie → decompile5Action → decompileActions → decompileSETTARGET|0.4.8|
||CVE-2018-20428|main → readMovie → outputBlock → outputSWF\_DOACTION → decompile5Action → decompileActions → strlenext|0.4.8|
||CVE-2018-7873|main → readMovie → outputBlock → outputSWF\_DEFINEBUTTON2 → decompile5Action → decompileActions →  decompileCALLMETHOD → newVar\_N → getString  (case PUSH\_INT: sprintf)|0.4.8|
||CVE-2018-7874|main → readMovie → outputBlock → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileGETVARIABLE → getName → strlenext|0.4.8|
||CVE-2018-7877|main → readMovie → outputBlock → outputSWF\_DEFINEBUTTON2 → decompile5Action → decompileActions →  decompileSingleArgBuiltInFunctionCall → newVar\_N → getString  (case PUSH\_BOOLEAN: act -> p.Boolean)|0.4.8|
||CVE-2019-16705|main → readMovie → outputBlock → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileIF → decompileSETTARGET → decompileGETTIME → OpCode|0.4.8|
||CVE-2020-6629|main → readMovie → outputBlock → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileGETURL2|0.4.8|
||CVE-2017-11732|main → readMovie → outputBlock → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileIMPLEMENTS → dcputs|0.4.8|
||CVE-2017-11733|main → readMovie → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileSTACKSWAP → stackswap|0.4.8|
||CVE-2017-11734|main → readMovie → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileCALLFUNCTION|0.4.8|
||CVE-2017-16883|main → readMovie → outputSWF\_DEFINETEXT2  → outputSWF\_TEXT\_RECORD|0.4.8|
||CVE-2018-11017|main → readMovie → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileSETTARGET → decompileCALLMETHOD → newVar\_N|0.4.8|
||CVE-2018-11095|main → readMovie → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileJUMP|0.4.8|
||CVE-2018-20591|main → readMovie → outputBlock → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileDEFINEFUNCTION → decompileJUMP|0.4.8|
||CVE-2018-6315|main → readMovie → outputBlock → outputSWF\_DEFINETEXT → outputSWF\_TEXT\_RECORD|0.4.8|
||CVE-2018-7867|main → readMovie → outputBlock → outputSWF\_INITACTION → decompile5Action → decompileActions → decompileIF → decompileArithmeticOp → getString  (case PUSH\_REGISTER: sprintf(t,"R%d", act -> p.RegisterNumber );)|0.4.8|
||CVE-2018-7868|main → readMovie → outputBlock → outputSWF\_INITACTION → decompile5Action → decompileActions → decompileIF → decompileDEFINEFUNCTION → decompileGETMEMBER → getName|0.4.8|
||CVE-2018-7870|main → readMovie → outputBlock → outputSWF\_DOACTION  → decompile5Action → decompileActions → decompileSETVARIABLE → decompilePUSHPARAM → getString  (case PUSH\_CONSTANT16:  t=malloc(strlenext(pool\[act->p.Constant16])+3);)|0.4.8|
||CVE-2018-7871|main → readMovie → outputBlock → outputSWF\_INITACTION → decompile5Action → decompileActions → decompileDEFINEFUNCTION → decompileGETVARIABLE → getName|0.4.8|
||CVE-2018-7875|main → readMovie → outputBlock → outputSWF\_INITACTION → decompile5Action → decompileActions → decompileIF → decompileDEFINEFUNCTION → decompileCALLMETHOD → newVar\_N → getString  (case PUSH\_CONSTANT: t=malloc(strlenext(pool\[act->p.Constant8])+3);)|0.4.8|
||CVE-2021-34342|main → readMovie → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileTRY → decompileSETTARGET → decompileNEWOBJECT → newVar\_N|0.4.8|
||CVE-2018-7872|main → readMovie → outputBlock → outputSWF\_INITACTION → decompile5Action → decompileActions → decompileIF → decompileDEFINEFUNCTION → decompileCALLMETHOD → getName|0.4.8|
||CVE-2018-9165|main → readMovie → outputBlock → outputSWF\_DEFINEBUTTON2 → decompile5Action → decompileActions → decompileCALLMETHOD → getName|0.4.8|
||CVE-2018-11226|main → readMovie → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileSETVARIABLE → getName → getString  (case PUSH\_INT: sprintf(t,"%ld", act->p.Integer );)|0.4.8|
||CVE-2019-9113|main → readMovie → outputSWF\_DOACTION → decompile5Action → decompileActions → decompileSETTARGET → decompileNEWOBJECT → newVar\_N → getString|0.4.8|
||**CVE-2023-23052**|**main → embed\_swf → newSWFPrebuiltClip\_fromInput → (openswf)**|**04aee52**|
||**CVE-2023-23053**|**main → makeswf\_compile\_source → SWFAction\_compile → swf5parse → (swf5lex)**|**04aee52**|
||**CVE-2023-23054**|**SWFShape\_drawCubic → SWFShape\_drawScaledCubicTo → (SWFShape\_approxCubic) → (subdivideCubic)**|**04aee52**|
||**CVE-2023-23051**|**main → makeswf\_compile\_source → SWFAction\_compile → swf5parse → newBuffer**|**04aee52**|
|**liblouis 13=10+3**|CVE-2017-13743|main → lou\_getTable → compileTranslationTable → compileFile → compileRule → getOpcode → \_lou\_showString|3.2.0|
||CVE-2017-13742|main → lou\_getTable → compileTranslationTable → compileFile → compileRule → (includeFile)|3.2.0|
||CVE-2017-13741|main → lou\_getTable → compileTranslationTable → compileFile → compileRule → (includeFile) → (compileBrailleIndicator)|3.2.0|
||CVE-2017-13740|main → lou\_getTable → compileTranslationTable → compileFile → compileRule → compileUplow → getRuleCharsText → parseChars|3.2.0|
||CVE-2017-13739|main → lou\_getTable → compileTranslationTable → compileFile → compileRule → (includeFile) → **\_lou\_defaultTableResolver →** (resolveSubtable)|3.2.0|
||CVE-2017-13738|\_lou\_getALine|3.2.0|
||CVE-2018-11440|main → lou\_getTable → compileTranslationTable → compileFile → compileRule → compileUplow → getRuleCharsText → parseChars|3.5.0|
||CVE-2018-11577|main → lou\_getTable → compileTranslationTable → compileFile → compileRule → compilePassOpcode → passGetDots → parseDots → compileError  → \_lou\_logMessage → lou\_logPrint|3.5.0|
||CVE-2018-11685|main → lou\_getTable → compileTranslationTable → compileFile → compileRule  → (compileHyphenation)|3.5.0|
||CVE-2018-17294|main → translate\_input → lou\_translateString → lou\_translate → \_lou\_translateWithTracing  → makeCorrections  → findForPassRule  → passDoTest  → (matchCurrentInput)|3.6.0|
||**CVE-2023-26767**|**lou\_setDataPath**|\*\*3.24.0 (6223f21) \*\*|
||**CVE-2023-26768**|**lou\_logFile**|\*\*3.24.0 (6223f21) \*\*|
||**CVE-2023-26769**|main → lou\_getTable → \_lou\_getTable  → getTable  → compileTable  → \_lou\_resolveTable  → **\_lou\_defaultTableResolver → (resolveSubtable)**|\*\*3.24.0 (6223f21) \*\*|



