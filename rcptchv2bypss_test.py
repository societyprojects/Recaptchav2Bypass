#!/usr/bin/env python3

from src.main import Rcptchv2Bypss

def main():
    solvec = Rcptchv2Bypss(page_timeout=10, headless_mode=False)
    response = solvec.solve_captcha(url="https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3Dsite%253A*.ru%2Binurl%253Adashboard%2B-www%26client%3Dfirefox-b-d%26sca_esv%3D581abf87ebc1492d%26ei%3DdRKPZ4PUDIec4-EPir3NqAM%26ved%3D0ahUKEwjD4pPb7YWLAxUHzjgGHYpeEzUQ4dUDCA8%26uact%3D5%26oq%3Dsite%253A*.ru%2Binurl%253Adashboard%2B-www%26gs_lp%3DEgxnd3Mtd2l6LXNlcnAiHnNpdGU6Ki5ydSBpbnVybDpkYXNoYm9hcmQgLXd3d0ixDlDEBVicDXABeACQAQCYASagAbsBqgEBNbgBA8gBAPgBAZgCAKACAJgDAIgGAZIHAKAH4QE%26sclient%3Dgws-wiz-serp&q=EgRnUUCRGPykvLwGIjCoxwO1en-GtCeCpfzBQwHYemTBmtlbEoUsDSfcB9HOWPhZQTFh7ghdsL48pjDtHYUyAXJaAUM")

    if response is not None:
        print(response.title, response.current_url)

if __name__ == '__main__':
  main()
