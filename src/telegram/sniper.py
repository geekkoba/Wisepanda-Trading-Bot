from telebot import types

from src.database import user as user_model
from src.engine import api as main_api
import threading

chain_gas_prices = [0.1, 0.2, 0.3]
chain_slippages = [5, 10, 20]
chain_limit_token_prices = [500, 1000, 2000]
chain_market_caps = [10000, 200000, 50000]
chain_liquidities = [10000, 200000, 50000]
chain_taxes = [5, 10, 20]

x_value_list = {"buy-amount": 0, "limit-token-price": 0, 'gas-price': 0, 'slippage': 0,
                "market-capital": 0, "liquidity": 0, "limit-tax": 0}

index_list = {'wallet': 100, 'buy_amount': 100, 'gas_price': 100, 'slippage': 100,
              'limit_token_price': 100, 'liquidity': 100,
              'tax': 100, 'market_cap': 100}

result = {'wallet': 0, 'token': '', 'buy_amount': 0, 'gas_price': 0, 'slippage': 0,
          'limit_token_price': 0, 'liquidity': 0, 'tax': 0, 'market_cap': 0}


def initialize_x_value():
    x_value_list['buy-amount'] = 0
    x_value_list['gas-amount'] = 0
    x_value_list['gas-price'] = 0
    x_value_list['limit-token-price'] = 0
    x_value_list['slippage'] = 0
    x_value_list['market-capital'] = 0
    x_value_list['liquidity'] = 0
    x_value_list['limit-tax'] = 0


def handle_sniper(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    text = '''
🛒 * Token Sniper*

Enter a token symbol or address to buy.
    '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))


def get_keyboard(update_data, chat_id, index_data):
   # wallet_count = 4
    # buy_count = 4
    # gas_amount_count = 3

    keyboard = types.InlineKeyboardMarkup()
    wallets = []

    chain_wallets = main_api.get_wallets(chat_id)
    wallet_count = len(chain_wallets)
    for index in range(wallet_count):
        caption = f'{"🟢" if index == index_data['wallet'] else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select buy wallet {index}")
        wallets.append(button)

    buys = []
    current_keyboards = main_api.get_keyboards(chat_id)
    chain_buy_amounts = current_keyboards['buy']
    buy_count = len(chain_buy_amounts)
    for index in range(buy_count):
        if index_data['buy_amount'] == 100:
            caption = f'💰{chain_buy_amounts[index]}Ξ'
        else:
            caption = f'{"🟢" if index == index_data['buy_amount'] else ""} 💰{
                chain_buy_amounts[index]}Ξ'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select buy amount {index}")
        buys.append(button)

    if update_data['buy-amount'] == 0:
        caption = "💰 XΞ"
    else:
        caption = f"🟢 💰 {update_data['buy-amount']}Ξ"
    buy_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select buy amount x')

    gas_prices = []
    gas_price_count = len(chain_gas_prices)
    for index in range(gas_price_count):
        if index_data['gas_price'] == 100:
            caption = f'{chain_gas_prices[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['gas_price'] else ""} {
                chain_gas_prices[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select gas price {index}")
        gas_prices.append(button)
    gas_price_title = types.InlineKeyboardButton(
        '----- Gas Price -----', callback_data='set title')
    if update_data['gas-price'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['gas-price']}"
    gas_price_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select gas price x')

    slippages = []
    slip_page_count = len(chain_slippages)
    for index in range(slip_page_count):
        if index_data['slippage'] == 100:
            caption = f'{chain_slippages[index]}%'
        else:
            caption = f'{" 🟢" if index == index_data['slippage'] else ""} {
                chain_slippages[index]}%'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select slippage {index}")
        slippages.append(button)
    slippage_title = types.InlineKeyboardButton(
        '----- Slippage -----', callback_data='set title')
    if update_data['slippage'] == 0:
        caption = "X %"
    else:
        caption = f"🟢 {update_data['slippage']}%"
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select slippage x')
# limit order
    limit_token_prices = []
    limit_token_price_count = len(chain_limit_token_prices)
    for index in range(limit_token_price_count):
        if index_data['limit_token_price'] == 100:
            caption = f'{chain_limit_token_prices[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['limit_token_price'] else ""} {
                chain_limit_token_prices[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select limit token price {index}")
        limit_token_prices.append(button)
    limit_token_price_title = types.InlineKeyboardButton(
        '----- Token Price -----', callback_data='set title')
    if update_data['limit-token-price'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['limit-token-price']}"
    limit_token_price_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select limit token price x')

    limit_taxes = []
    limit_tax_count = len(chain_taxes)
    for index in range(limit_tax_count):
        if index_data['tax'] == 100:
            caption = f'{chain_taxes[index]}%'
        else:
            caption = f'{" 🟢" if index == index_data['tax'] else ""} {
                chain_taxes[index]}%'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select limit tax {index}")
        limit_taxes.append(button)
    limit_tax_title = types.InlineKeyboardButton(
        '----- Tax -----', callback_data='set title')
    if update_data['limit-tax'] == 0:
        caption = "X %"
    else:
        caption = f"🟢 {update_data['limit-tax']}%"
    limit_tax_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select limit tax x')

    market_capitals = []
    market_capital_count = len(chain_market_caps)
    for index in range(market_capital_count):
        if index_data['market_cap'] == 100:
            caption = f'{chain_market_caps[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['market_cap'] else ""} {
                chain_market_caps[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select market capital {index}")
        market_capitals.append(button)
    market_capital_title = types.InlineKeyboardButton(
        '-----Max Market Capital -----', callback_data='set title')
    if update_data['market-capital'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['market-capital']}"
    market_capital_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select market capital x')

    liquidities = []
    liquidity_count = len(chain_liquidities)
    for index in range(liquidity_count):
        if index_data['liquidity'] == 100:
            caption = f'{chain_liquidities[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['liquidity'] else ""} {
                chain_liquidities[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select liquidity {index}")
        liquidities.append(button)
    liquidity_title = types.InlineKeyboardButton(
        '-----Min Liquidity -----', callback_data='set title')
    if update_data['liquidity'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['liquidity']}"
    liquidity_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select liquidity x')

    create_order = types.InlineKeyboardButton(
        '✔️ Set Sniper', callback_data='make sniper order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(*wallets[0:(wallet_count)])

    keyboard.row(*buys[0:(buy_count // 2)])
    keyboard.row(*buys[(buy_count // 2):buy_count], buy_x)

    keyboard.row(gas_price_title)
    keyboard.row(*gas_prices[0:(len(gas_prices))], gas_price_x)
    keyboard.row(slippage_title)
    keyboard.row(*slippages[0:(len(slippages))], slippage_x)

    keyboard.row(limit_token_price_title)
    keyboard.row(
        *limit_token_prices[0:(len(limit_token_prices))], limit_token_price_x)
    keyboard.row(market_capital_title)
    keyboard.row(
        *market_capitals[0:(len(market_capitals))], market_capital_x)
    keyboard.row(liquidity_title)
    keyboard.row(
        *liquidities[0:(len(liquidities))], liquidity_x)
    keyboard.row(limit_tax_title)
    keyboard.row(
        *limit_taxes[0:(len(limit_taxes))], limit_tax_x)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard


def handle_input_token(bot, message):
   # user = user_model.get_user_by_telegram(message.chat.id)

    token = 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7

    chain = 'ethereum'

    name = "elo"

    text = f'''
            *Token Buy*

    Sell your tokens here.

  *{name}  (🔗{chain})*
  {token}
  ❌ Snipe not set

  [Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
      '''
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def select_buy_wallet(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]'
    index_list['wallet'] = int(index)
    result['wallet'] = int(index)

    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_buy_amount(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    index_list['buy_amount'] = int(index)
    keyboards = main_api.get_keyboards(message.chat.id)
    result['buy_amount'] = keyboards['buy'][int(index)]
    x_value_list['buy-amount'] = 0

    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_gas_price(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    index_list['gas_price'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['gas_price'] = chain_gas_prices[int(index)]
    x_value_list['gas-price'] = 0
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_slip_page(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    index_list['slippage'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['slippage'] = chain_slippages[int(index)]
    x_value_list['slippage'] = 0
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_limit_token_price(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    index_list['limit_token_price'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['limit_token_price'] = chain_limit_token_prices[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    x_value_list['limit-token-price'] = 0
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_limit_tax(bot, message, index):
  #  user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['limit-tax'] = 0
    index_list['tax'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['tax'] = chain_taxes[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_market_capital(bot, message, index):
  #  user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['market-capital'] = 0
    index_list['market_cap'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['market_cap'] = chain_market_caps[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_liquidity(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['liquidity'] = 0
    index_list['liquidity'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['liquidity'] = chain_liquidities[int(index)]
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_buy_amount_x(bot, message):
    text = '''
*Token Buy > 💰 XΞ*
Enter the amount to buy:
'''
    item = "Buy Amount"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_gas_price_x(bot, message):
    text = '''
*Token Buy > ⛽ X*
Enter the gas price to set:
'''
    item = "Gas Price"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_slippage_x(bot, message):
    text = '''
*Token Buy > 💧 X%*
Enter the slippage to set:
'''
    item = "Slippage"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_limit_token_price_x(bot, message):
    text = '''
*Token Buy > 💰 X*
Enter the Token Price to set:
'''
    item = "Token Price"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_market_capital_x(bot, message):
    text = '''
*Token Buy > 💰 X*
Enter the Maximum Market Capital to set:
'''
    item = "Market Capital"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_liquidity_x(bot, message):
    text = '''
*Token Buy > 💰 X*
Enter the liquidity to set:
'''
    item = "Liquidity"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_limit_tax_x(bot, message):
    text = '''
*Token Buy > 💰 X%*
Enter the tax to set:
'''
    item = "Tax"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_duration_x(bot, message):
    text = '''
*Token Buy > 🕞 X*
Enter the duration to set:
'''
    item = "Duration"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_input_value(bot, message, item):
    if item == "Buy Amount":
        buy_amount_x = float(message.text)
        x_value_list['buy-amount'] = buy_amount_x
        result['buy_amount'] = buy_amount_x
        index_list['buy_amount'] = 100
    elif item == "Gas Price":
        gas_price_x = float(message.text)
        x_value_list['gas-price'] = gas_price_x
        result['gas_price'] = gas_price_x
        index_list['gas_price'] = 100
    elif item == "Slippage":
        slippage_x = float(message.text)
        x_value_list['slippage'] = slippage_x
        result['slippage'] = slippage_x
        index_list['slippage'] = 100
    elif item == "Token Price":
        token_price_x = float(message.text)
        x_value_list['limit-token-price'] = token_price_x
        result['limit_token_price'] = token_price_x
        index_list['limit_token_price'] = 100
    elif item == "Market Capital":
        market_capital_x = float(message.text)
        x_value_list['market-capital'] = market_capital_x
        result['market_cap'] = market_capital_x
        index_list['market_cap'] = 100
    elif item == "Liquidity":
        slippage_x = float(message.text)
        x_value_list['liquidity'] = slippage_x
        result['liquidity'] = slippage_x
        index_list['liquidity'] = 100
    elif item == "Tax":
        slippage_x = float(message.text)
        x_value_list['limit-tax'] = slippage_x
        result['tax'] = slippage_x
        index_list['tax'] = 100

    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    token = 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7

    chain = 'ethereum'

    name = "elo"
    text = f'''
            *Token Buy*

    Sell your tokens here.

     *{name}  (🔗{chain})*
      {token}
      ❌ Snipe not set

      [Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
          '''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_set_sniper(bot, message):
    chain_index = main_api.get_current_chain_index(message.chat.id)
    chains = main_api.get_supported_chains()
    result['token'] = chains[chain_index]
    main_api.token_sniper(message.chat.id, result)
    bot.send_message(chat_id=message.chat.id,
                     text='Successfully registered Sniper')
