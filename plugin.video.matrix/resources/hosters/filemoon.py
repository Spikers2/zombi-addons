#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filemoon', 'filemoon')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()

        api_call = False

        sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = 'file:"(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               url = aResult[1][0] # fichier master valide pour la lecture
               oRequestHandler = cRequestHandler(url)
               sHtmlContent2 = oRequestHandler.request()
               list_url = []
               list_q = []
               oParser = cParser()
               sPattern = 'PROGRAM.*?BANDWIDTH.*?RESOLUTION=(\d+x\d+).*?(https.*?m3u8)'
               aResult = oParser.parse(sHtmlContent2, sPattern)
               if aResult[0]:
                  for aEntry in aResult[1]:
                      list_url.append(aEntry[1])
                      list_q.append(aEntry[0])
                  if list_url:
                     api_call = dialog().VSselectqual(list_q, list_url)

        else:
            sPattern = 'file:"([^"]+)",label:"[0-9]+"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                # initialisation des tableaux
                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                api_call = dialog().VSselectqual(qua, url + '|User-Agent=' + UA)


        if api_call:
            return True, api_call

        return False, False
