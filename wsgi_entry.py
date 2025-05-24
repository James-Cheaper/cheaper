from webscraper.main import main

def application(environ, start_response):

    main()
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b"Scraping complete.\n"]
