"""
TCGPlayer reprice tool.

Usage
-----
python reprice.py filename.csv
"""
import sys
import csv


class CardData:
    """Takes one row from CSV and converts it into values referenced by column name."""

    def __init__(self, row: list):
        (
            self.tcgplayer_id,
            self.product_line,
            self.set_name,
            self.product_name,
            self.title,
            self.number,
            self.rarity,
            self.condition,
            self.tcg_market_price,
            self.tcg_direct_low,
            self.tcg_low_price_with_shipping,
            self.tcg_low_price,
            self.total_quantity,
            self.add_to_quantity,
            self.tcg_marketplace_price,
            self.photo_url,
        ) = row

        for varname in [
            "tcg_market_price",
            "tcg_direct_low",
            "tcg_low_price_with_shipping",
            "tcg_low_price",
            "total_quantity",
            "add_to_quantity",
            "tcg_marketplace_price"
        ]:
            varvalue = getattr(self, varname)
            if varvalue != "":
                setattr(self, varname, float(varvalue))


def price_formula(card_data: CardData):
    """
    TODO Enter the formula that will determine you're prices here!
    """
    # TCGPlayer direct repricer based on max(market price, direct price) w/ floor set by min price.
    # Market price offset according to https://mktg-assets.tcgplayer.com/web/seller/guides/TCGplayer-Direct-Shipping-Replacement-Costs.pdf
    MIN_PRICE = .09

    tcg_marketplace_price = card_data.tcg_marketplace_price if card_data.tcg_marketplace_price != "" else -1
    tcg_market_price = card_data.tcg_market_price if card_data.tcg_market_price != "" else -1
    tcg_direct_low = card_data.tcg_direct_low if card_data.tcg_direct_low != "" else -1

    if tcg_marketplace_price > 42 or tcg_market_price > 42:
        return max(tcg_marketplace_price, tcg_market_price + 1)

    if tcg_marketplace_price > 20 or tcg_market_price > 20:
        return max(tcg_marketplace_price, tcg_market_price + 3)

    if tcg_direct_low > 3 or tcg_market_price > 3:
        return max(tcg_direct_low, tcg_market_price + 0.3)

    return max(tcg_direct_low, tcg_market_price + 0.03, MIN_PRICE)


if __name__ == '__main__':
    filename_input = sys.argv[1]
    filename_output = filename_input.replace(".", "_repriced.")

    with open(filename_output, "w", newline="", encoding="utf8") as fileout:
        csvout = csv.writer(fileout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        with open(filename_input, "r", newline="", encoding="utf8") as filein:
            csvin = csv.reader(filein, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for i, row in enumerate(csvin):
                if i > 0:
                    row[-2] = f"{price_formula(CardData(row)):.2f}"

                csvout.writerow(row)
