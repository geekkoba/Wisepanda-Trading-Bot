from src.database import user as user_model

def add_user(user_id):
  user_model.add(user_id)

def get_user(user_id):
  return user_model.get(user_id)

def get_chain(user_id):
  user = get_user(user_id)
  return user.chain

def set_chain(user_id, chain):
  user_model.set(user_id, 'chain', chain)

def get_wallets(user_id, chain):
  user = get_user(user_id)
  return user.wallets[chain]

def add_wallet(user_id, chain, wallet):
  user = get_user(user_id)
  user.wallets[chain].append(wallet)
  user_model.set(user_id, 'wallets', user.wallets)

def remove_wallet(user_id, chain, wallet_id):
  user = get_user(user_id)
  for index, wallet in enumerate(user.wallets[chain]):
    if wallet['id'] == wallet_id:
      user.wallets[chain].pop(index)
      break
  user_model.set(user_id, 'wallets', user.wallets)

def get_token_snipers(user_id, chain):
  user = get_user(user_id)
  return list(filter(lambda token_sniper: token_sniper['chain'] == chain, user.token_snipers))

def add_token_sniper(user_id, token_sniper):
  user = get_user(user_id)
  user.token_snipers.append(token_sniper)
  user_model.set(user_id, 'token_snipers', user.token_snipers)

def get_token_sniper(user_id, token_sniper_id):
  user = get_user(user_id)
  for token_sniper in user.token_snipers:
    if token_sniper['id'] == token_sniper_id:
      return token_sniper
  return None

def set_token_sniper(user_id, token_sniper_id, token_sniper):
  user = get_user(user_id)
  for index, token_sniper in enumerate(user.token_snipers):
    if token_sniper['id'] == token_sniper_id:
      user.token_snipers[index] = token_sniper
      break
  user_model.set(user_id, 'token_snipers', user.token_snipers)

def remove_token_sniper(user_id, token_sniper_id):
  user = get_user(user_id)
  for index, token_sniper in enumerate(user.token_snipers):
    if token_sniper['id'] == token_sniper_id:
      user.token_snipers.pop(index)
      break
  user_model.set(user_id, 'token_snipers', user.token_snipers)

def get_limit_orders(user_id, chain):
  user = get_user(user_id)
  return list(filter(lambda limit_order: limit_order['chain'] == chain, user.limit_orders))

def add_limit_order(user_id, limit_order):
  user = get_user(user_id)
  user.limit_orders.append(limit_order)
  user_model.set(user_id, 'limit_orders', user.limit_orders)

def get_limit_order(user_id, limit_order_id):
  user = get_user(user_id)
  for limit_order in user.limit_orders:
    if limit_order['id'] == limit_order_id:
      return limit_order
  return None

def set_limit_order(user_id, limit_order_id, limit_order):
  user = get_user(user_id)
  for index, limit_order in enumerate(user.limit_orders):
    if limit_order['id'] == limit_order_id:
      user.limit_orders[index] = limit_order
      break
  user_model.set(user_id, 'limit_orders', user.limit_orders)

def remove_limit_order(user_id, limit_order_id):
  user = get_user(user_id)
  for index, limit_order in enumerate(user.limit_orders):
    if limit_order['id'] == limit_order_id:
      user.limit_orders.pop(index)
      break
  user_model.set(user_id, 'limit_orders', user.limit_orders)

def get_dca_orders(user_id, chain):
  user = get_user(user_id)
  return list(filter(lambda dca_order: dca_order['chain'] == chain, user.dca_orders))

def add_dca_order(user_id, dca_order):
  user = get_user(user_id)
  user.dca_orders.append(dca_order)
  user_model.set(user_id, 'dca_orders', user.dca_orders)

def get_dca_order(user_id, dca_order_id):
  user = get_user(user_id)
  for dca_order in user.dca_orders:
    if dca_order['id'] == dca_order_id:
      return dca_order
  return None

def set_dca_order(user_id, dca_order_id, dca_order):
  user = get_user(user_id)
  for index, dca_order in enumerate(user.dca_orders):
    if dca_order['id'] == dca_order_id:
      user.dca_orders[index] = dca_order
      break
  user_model.set(user_id, 'dca_orders', user.dca_orders)

def remove_dca_order(user_id, dca_order_id):
  user = get_user(user_id)
  for index, dca_order in enumerate(user.dca_orders):
    if dca_order['id'] == dca_order_id:
      user.dca_orders.pop(index)
      break
  user_model.set(user_id, 'dca_orders', user.dca_orders)

def get_positions(user_id, chain):
  user = get_user(user_id)
  return list(filter(lambda position: position['chain'] == chain, user.positions))

def add_position(user_id, position):
  user = get_user(user_id)
  user.positions.append(position)
  user_model.set(user_id, 'positions', user.positions)

def get_position(user_id, position_id):
  user = get_user(user_id)
  for position in user.positions:
    if position['id'] == position_id:
      return position
  return None

def set_position(user_id, position_id, position):
  user = get_user(user_id)
  for index, position in enumerate(user.positions):
    if position['id'] == position_id:
      user.positions[index] = position
      break
  user_model.set(user_id, 'positions', user.positions)

def remove_position(user_id, position_id):
  user = get_user(user_id)
  for index, position in enumerate(user.positions):
    if position['id'] == position_id:
      user.positions.pop(index)
      break
  user_model.set(user_id, 'positions', user.positions)
