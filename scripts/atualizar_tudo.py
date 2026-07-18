import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import logger


# Scripts executados em ordem
SCRIPTS = [

    "update.py",

    "cotacoes.py",

    "dividendos.py",

    "segmentos.py",

    "indicadores.py",

    "validar.py"

]


BASE_DIR = Path(__file__).resolve().parent.parent

STATUS_FILE = BASE_DIR / "docs" / "status.json"



def agora_utc():

    return datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )



def salvar_status(
    status,
    tempo=None,
    erro=None
):

    dados = {

        "ultima_atualizacao":
            agora_utc(),

        "status":
            status,

        "tempo_segundos":
            tempo,

        "erro":
            erro

    }


    with open(
        STATUS_FILE,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )



def executar(script):

    logger.info(
        f"Executando {script}"
    )


    inicio = time.time()


    resultado = subprocess.run(
        [
            sys.executable,
            str(
                BASE_DIR /
                "scripts" /
                script
            )
        ]
    )


    tempo = (
        time.time()
        -
        inicio
    )


    if resultado.returncode != 0:

        logger.aviso(
            f"Falha em {script}"
        )

        return False, tempo


    logger.info(
        f"{script} concluído em {tempo:.2f}s"
    )


    return True, tempo



def main():

    logger.linha()


    logger.info(
        "INICIANDO ATUALIZAÇÃO COMPLETA"
    )


    inicio_total = time.time()


    try:


        for script in SCRIPTS:


            sucesso, tempo = executar(
                script
            )


            if not sucesso:


                tempo_total = (
                    time.time()
                    -
                    inicio_total
                )


                salvar_status(
                    "ERRO",
                    round(
                        tempo_total,
                        2
                    ),
                    f"Falha em {script}"
                )


                logger.aviso(
                    "Atualização interrompida"
                )


                return



        tempo_total = (
            time.time()
            -
            inicio_total
        )


        salvar_status(
            "OK",
            round(
                tempo_total,
                2
            )
        )


        logger.info(
            "TODAS AS ETAPAS CONCLUÍDAS"
        )


        logger.info(
            f"Tempo total: {tempo_total:.2f}s"
        )



    except Exception as erro:


        tempo_total = (
            time.time()
            -
            inicio_total
        )


        salvar_status(
            "ERRO",
            round(
                tempo_total,
                2
            ),
            str(erro)
        )


        logger.aviso(
            f"Erro geral: {erro}"
        )



    logger.linha()



if __name__ == "__main__":

    main()