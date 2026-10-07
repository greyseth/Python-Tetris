from unicodedata import numeric

import pygame as pg

import block_data


class Block:
    def __init__(self, blockType, onGameLose):
        self.tiles = []
        self.isPlaced = False

        # Sets game over callback function
        self.onGameLose = onGameLose

        _blockType = blockType
        if isinstance(blockType, int):
            match blockType:
                case 0:
                    _blockType = "I"
                case 1:
                    _blockType = "J"
                case 2:
                    _blockType = "L"
                case 3:
                    _blockType = "T"
                case 4:
                    _blockType = "O"
                case 5:
                    _blockType = "S"
                case 6:
                    _blockType = "Z"

        for y, row in enumerate(block_data.TETROMINOS[_blockType]):
            for x, isTile in enumerate(row):
                if isTile:
                    self.tiles.append(
                        [3 + x, y]
                    )  # Spawns new block with a left margin of 3

    def checkBounds(self, direction, placedTiles):
        ret = True

        for _, tile in enumerate(self.tiles):
            if [int(tile[0] + direction), int(tile[1])] in map(
                lambda t: [int(t[0]), int(t[1])], placedTiles
            ):
                ret = False
                break

            if direction == 1:
                ret = not tile[0] >= 10 - 1
            else:
                ret = not tile[0] <= 0 + 1

        return ret

    def moveTilesHorizontal(self, direction, placedTiles):
        if not self.checkBounds(direction, placedTiles):
            return
        for i, tile in enumerate(self.tiles):
            self.tiles[i] = [tile[0] + direction, tile[1]]

    def checkIsPlaced(self, placedTiles, b):
        lowestTile = 0

        for _, tile in enumerate(self.tiles):
            if [int(tile[0]), int(tile[1])] in map(
                lambda t: [int(t[0]), int(t[1])], placedTiles
            ):
                self.isPlaced = True

            if tile[1] > lowestTile:
                lowestTile = tile[1]

        if not self.isPlaced and lowestTile >= 20:
            self.isPlaced = True

        if self.isPlaced:
            # moves tiles up by one
            for i, tile in enumerate(self.tiles):
                self.tiles[i] = [tile[0], tile[1] - 1]
                print(int(tile[1]))
                if int(tile[1]) <= 2:
                    self.onGameLose()

            # appends to placedTiles
            for tile in self.tiles:
                placedTiles.append(tile)

            return None
        else:
            return b

    def advanceBlock(self, speed, deltaTime, placedTiles, blocks):
        for i, tile in enumerate(self.tiles):
            self.tiles[i] = [tile[0], tile[1] + speed / (deltaTime * 100)]

        return self.checkIsPlaced(placedTiles, blocks)

    def drawBlock(self, screen, leftStart, topStart, tileSize):
        for _, tile in enumerate(self.tiles):
            posX = tile[0]
            posY = int(tile[1])

            r = (
                leftStart + posX * tileSize,
                topStart + posY * tileSize,
                tileSize,
                tileSize,
            )

            pg.draw.rect(screen, "Red", r)
            pg.draw.rect(screen, "White", r, 1)
