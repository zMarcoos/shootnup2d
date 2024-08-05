RESOURCES_PATH = './resources/'
ASSETS_PATH = f'{RESOURCES_PATH}./assets/'
ENTITIES_PATH = f'{ASSETS_PATH}entities/'
SHOOT_PATH = f'{ASSETS_PATH}shoot/'
SOUNDS_PATH = f'{ASSETS_PATH}sounds/'
PARTICLES_PATH = f'{ASSETS_PATH}particles/'
ITEMS_PATH = f'{ASSETS_PATH}items/'

SHIPS = {
  'player': {
    'texture': f'{ENTITIES_PATH}player.png',
    'sprites_size': (128, 128),
    'shoot_texture': f'{SHOOT_PATH}player_shoot.png',
    'double_shoot_texture': f'{SHOOT_PATH}player_double_shoot.png',
    'special_shoot_texture': f'{SHOOT_PATH}special_shoot.png',
    'special_sprites_size': (100, 100),
    'velocity': 0.1,
    'health': 10
  },
  'player_special': {
    'texture': f'{ENTITIES_PATH}player_special.png',
    'sprites_size': (128, 128)
  },
  'enemy': [
    {
      'texture': f'{ENTITIES_PATH}blue_enemy.png',
      'sprites_size': (100, 100),
      'shoot_texture': f'{SHOOT_PATH}blue_enemy_shoot.png',
      'velocity': 0.03,
      'health': 1
    },
    {
      'texture': f'{ENTITIES_PATH}green_enemy.png',
      'sprites_size': (128, 128),
      'shoot_texture': f'{SHOOT_PATH}green_enemy_shoot.png',
      'velocity': 0.03,
      'health': 1
    },
    {
      'texture': f'{ENTITIES_PATH}yellow_enemy.png',
      'sprites_size': (100, 100),
      'shoot_texture': f'{SHOOT_PATH}yellow_enemy_shoot.png',
      'velocity': 0.03,
      'health': 1
    }
  ],
  'boss': {
    'texture': f'{ENTITIES_PATH}boss.png',
    'sprites_size': (100, 100),
    'shoot_texture': f'{SHOOT_PATH}player_shoot.png',
    'velocity': 0.05,
    'health': 20
  }
}

EFFECTS = {
  'smoke': {
    'texture': f'{PARTICLES_PATH}smoke.png',
    'sprites_size': (100, 100)
  }
}

ITEMS = {
  'habilities': {
    'texture': f'{ITEMS_PATH}habilities.png',
    'sprites_size': (100, 100)
  }
}

SOUNDS = {
  'background': f'{SOUNDS_PATH}background.wav'
}