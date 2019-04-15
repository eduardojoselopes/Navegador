class ProcessaDadosURL:
    def __init__(self, url):
        self.url = url


    #Função para testar se url é válida.


    def le_url(self):
        if 'http://' in self.url:
            url = self.url.split("http://")

            if len(url) > 1:
                url.pop(0)
                url = url[0]
            return url
        if 'www' in self.url:
            url = self.url.split("www")
            if len(url) > 1:
                url.pop(0)
                url = url[0][1:]
            return url
        return self.url

    def separa_nome_diretorio(self):
        url = self.le_url()
        tamanho_nome = 0
        for i in range(len(url)):
            tamanho_nome += 1
            if url[i] == '/':
                break

        nome_do_site = []
        diretorio = []
        for i in range(len(url)):
            if i < tamanho_nome:
                nome_do_site.append(url[i])
            else:
                diretorio.append(url[i])

        nome_do_site.pop()
        nome_do_site = ''.join(nome_do_site)
        diretorio = ''.join(diretorio)
        return nome_do_site, diretorio


ProcessaDadosURL('www.ufsj.edu.br/portal/').separa_nome_diretorio()