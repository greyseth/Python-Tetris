import pygame as pg

import block
from block_data import TETROMINOS

pg.init()
screen = pg.display.set_mode((720, pg.display.Info().current_h - 50))
pg.display.set_caption("PyTris")

clock = pg.time.Clock()

deltaTime = 0
gameStartDelay = 0.1

tileSize = 50
tileBorderWidth = 1

runningBlock = None
tileDropSpeed = 0.04
tileDropSpeedFast = 0.35
tileMoveInterval = 0.1

placedTiles = []

tileMoveCount = 0


def gameOver():
    global placedTiles
    placedTiles = []
    spawnNewBlock()


def spawnNewBlock():
    return block.Block(1, onGameLose=gameOver)


running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("Black")

    areaWidth = tileSize * 10
    areaHeight = tileSize * 20

    leftStart = screen.get_width() / 2 - areaWidth / 2
    topStart = screen.get_height() / 2 - areaHeight / 2 - 10

    if runningBlock == None:
        runningBlock = spawnNewBlock()

    # Draws the background tiles
    for y in range(20):
        for x in range(10):
            bgRect = pg.Surface((tileSize, tileSize))
            bgRect.set_alpha(128)
            pg.draw.rect(
                bgRect, "White", bgRect.get_rect(), tileBorderWidth
            )  # define rectangle lines
            screen.blit(
                bgRect, (leftStart + x * tileSize, topStart + y * tileSize)
            )  # define position of rectangle (left, top)

    # Draws the placed tiles
    for _, tile in enumerate(placedTiles):
        pg.draw.rect(
            screen,
            "White",
            (
                leftStart + tile[0] * tileSize,
                topStart + int(tile[1]) * tileSize,
                tileSize,
                tileSize,
            ),
        )

    # Draws every block
    if not runningBlock.isPlaced:
        runningBlock.drawBlock(screen, leftStart, topStart, tileSize)

    _tileDropSpeed = tileDropSpeed

    # Handles keyboard inputs
    keys = pg.key.get_pressed()
    if tileMoveCount <= 0:
        if keys[pg.K_a]:
            runningBlock.moveTilesHorizontal(-1, placedTiles)

            tileMoveCount = tileMoveInterval
        elif keys[pg.K_d]:
            runningBlock.moveTilesHorizontal(1, placedTiles)

            tileMoveCount = tileMoveInterval
        else:
            tileMoveCount = 0

        if keys[pg.K_s]:
            _tileDropSpeed = tileDropSpeedFast

    if gameStartDelay > 0:
        gameStartDelay -= deltaTime
    else:
        gameStartDelay = 0

        # Manages block advancement
        if not runningBlock.isPlaced:
            # print("making block move down " + str(i))
            runningBlock = runningBlock.advanceBlock(
                _tileDropSpeed, deltaTime, placedTiles, runningBlock
            )

    tileMoveCount -= deltaTime

    # Refreshes display and updates deltaTime value
    pg.display.flip()
    deltaTime = clock.tick(60) / 1000

pg.quit()
