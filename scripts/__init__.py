# import scripts.add_card as add_card
# import scripts.query_price as query_price
from scripts.util import sanitize_string, create_directory, send_response
from scripts.add_card_scripts import parse_list, select_card, append_query
from scripts.query_price_scripts import check_set_promo, append_cards

from scripts.add_card import add_card
from scripts.query_price import query_price