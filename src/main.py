import argparse
import logging
import os
from dataclasses import asdict

from dotenv import load_dotenv
from iso4217 import Currency as ISO_Currency

from src.config import NBP_BASE_URL, PROJECT_ROOT
from src.connectors.database import DatabaseConnector
from src.currency import Currency
from src.data_source.local import LocalSource
from src.data_source.nbp import NbpSource

logging.basicConfig(
    format="%(asctime)s - %(name)s:%(lineno)s - [%(levelname)8s]: %(message)s",
    level=logging.INFO,
)
LOG = logging.getLogger(__name__)
load_dotenv(override=True)


def parse_arguments() -> argparse.Namespace:
    """_summary_

    Returns:
        argparse.Namespace: _description_
    """
    parser = argparse.ArgumentParser(
        prog="Currency Converter", description="Converts given currencies to PLN"
    )
    parser.add_argument(
        "-a", "--amount", type=float, required=True, help="Amount of money to convert to PLN"
    )
    parser.add_argument(
        "-c",
        "--currency",
        type=str.upper,
        choices=[currency.code for currency in ISO_Currency],
        required=True,
        help="Source currency",
    )
    parser.add_argument(
        "-s",
        "--source",
        type=str.upper,
        choices=["LOCAL", "NBP"],
        default="NBP",
        help="Data source used for conversion",
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to a file when source is LOCAL",
        default="example_currency_rates.json",
    )

    parser.add_argument(
        "-e",
        "--env",
        type=str.upper,
        choices=["DEV", "PROD"],
        help="Environment",
        default=os.getenv("ENVIRONMENT", "PROD"),
    )

    parser.add_argument("--debug", action="store_true", help="Whether to run in a debug mode")

    return parser.parse_args()


def get_currency(args: argparse.Namespace) -> Currency:
    """_summary_

    Args:
        args (argparse.Namespace): _description_

    Raises:
        Exception: _description_

    Returns:
        Currency: _description_
    """
    match args.source:
        case "LOCAL":
            currency = LocalSource(args.file).get_currency(args.currency)
        case "NBP":
            currency = NbpSource().get_currency(args.currency)
        case _:
            raise Exception("Source not available... yet")
    return currency


def main():  # pylint: disable=inconsistent-return-statements
    """_summary_"""
    try:
        args = parse_arguments()
        LOG.info(
            f"Converting {args.amount} {args.currency} to PLN using "
            f"{PROJECT_ROOT.joinpath(args.file) if args.source == 'LOCAL' else NBP_BASE_URL} "
            "as a source."
        )

        currency = get_currency(args)
        LOG.info(f"Currency rate: {currency.rate} (fetch date: {currency.date})")

        converted = currency.convert_to_pln(price=args.amount)
        LOG.info(f"Converted to PLN: {asdict(converted)['price_in_pln']:.2f}")

        DatabaseConnector(args.env).connector.save(converted)
        LOG.info("Job done!")
        return converted
    except Exception:
        LOG.error("Failed to convert currency", exc_info=args.debug)


if __name__ == "__main__":
    main()
