import pygame
import games
import heuristic

game = games.ConnectFour()
state = game.initial

player = 'X'
player2_log = ""
player_log = "Comienza el juego!"
cpu_log = ""
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
width = 20
height = 20
margin = 5
hint_flag = 0
grid = []
for x in range(7):
    grid.append([])
    for y in range(6):
        grid[x].append(0)

pygame.init()
hints = 5
pantalla = pygame.display.set_mode([700, 500])

pygame.display.set_caption("Connect 4")

done = False
hint_move = (0, 0)
reloj = pygame.time.Clock()

mode = 1
difficult = 1
fuente = pygame.font.Font(None, 36)

show_intro = True
intro_page = 1

while not done and show_intro:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            done = True
        if evento.type == pygame.MOUSEBUTTONDOWN:
            intro_page += 1
            if intro_page == 3:
                show_intro = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_m:
                mode += 1
                if mode == 5:
                    mode = 1

    pantalla.fill(black)

    if intro_page == 1:
        texto = fuente.render("4 en raya", True, white)
        pantalla.blit(texto, [10, 10])

        texto = fuente.render("Realizado por:", True, red)
        pantalla.blit(texto, [500, 400])

        texto = fuente.render("Alvaro Falcon Morales", True, white)
        pantalla.blit(texto, [400, 445])
        texto = fuente.render("Stefan Hautz", True, white)
        pantalla.blit(texto, [400, 470])

    if intro_page == 2:
        texto = fuente.render("Pulse m para cambiar la modalidad", True, white)
        pantalla.blit(texto, [10, 10])
        texto = fuente.render("Y de click para empezar!", True, white)
        pantalla.blit(texto, [10, 35])
        if mode == 1:
            texto = fuente.render("Modo: Multiplayer", True, white)
            pantalla.blit(texto, [10, 90])
        if mode == 2:
            texto = fuente.render("Modo: vs CPU", True, white)
            pantalla.blit(texto, [10, 90])
            texto = fuente.render("Dificultad: Facil", True, white)
            difficult = 1
            pantalla.blit(texto, [10, 120])
        if mode == 3:
            texto = fuente.render("Modo: vs CPU", True, white)
            pantalla.blit(texto, [10, 90])
            texto = fuente.render("Dificultad: Medio", True, white)
            difficult = 5
            pantalla.blit(texto, [10, 120])
        if mode == 4:
            texto = fuente.render("Modo: vs CPU", True, white)
            pantalla.blit(texto, [10, 90])
            texto = fuente.render("Dificultad: Dificil", True, white)
            difficult = 10
            pantalla.blit(texto, [10, 120])

    reloj.tick(20)

    pygame.display.flip()

while not done:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho = True
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_h:
                if hints > 0:
                    hint_move = games.alphabeta_search(state, game, d=6, cutoff_test=None,
                                                       eval_fn=heuristic.compute_utility(state))
                    hints -= 1
                    print hint_move
                    hint_flag = 1
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if mode == 1:
                pos = pygame.mouse.get_pos()
                y = pos[0] // (width + margin)
                x = pos[1] // (height + margin)
                if grid[x][y] == 0 and (x, y) in state.moves:
                    state = game.make_move((x, y), state)
                    if player == 'X':
                        grid[x][y] = 1
                        player = 'O'
                        player_log = "El jugador '"+str(player)+"' ha movido en la posicion: " + str((x, y))
                    else:
                        grid[x][y] = 2
                        player = 'X'
                        player2_log = "El jugador '"+str(player)+"' ha movido en la posicion: " + str((x, y))
            else:
                if player == 'X':
                    pos = pygame.mouse.get_pos()
                    y = pos[0] // (width + margin)
                    x = pos[1] // (height + margin)
                    if grid[x][y] == 0 and (x, y) in state.moves:
                        state = game.make_move((x, y), state)
                        grid[x][y] = 1
                        player = 'O'
                        player_log = "El jugador ha movido en la posicion: " + str((x, y))
    pantalla.fill(black)
    for x in range(7):
        for y in range(6):
            color = white
            if grid[x][y] == 1:
                color = blue
            elif grid[x][y] == 2:
                color = red
            pygame.draw.rect(pantalla,
                             color,
                             [(margin + width) * y + margin,
                              (margin + height) * x + margin,
                              width,
                              height])
    texto = fuente.render("Pulsa 'H' para obtener una pista", True, white)
    pantalla.blit(texto, [0, 180])
    texto = fuente.render("Pistas restantes: " + str(hints), True, red)
    pantalla.blit(texto, [0, 210])
    texto = fuente.render(player_log, True, blue)
    pantalla.blit(texto, [160, 0])
    texto = fuente.render(player2_log, True, red)
    pantalla.blit(texto, [160, 25])
    texto = fuente.render(cpu_log, True, red)
    pantalla.blit(texto, [160, 20])
    texto = fuente.render("Turno del jugador '" + str(player) + "'", True, white)
    pantalla.blit(texto, [0, 470])

    if hint_flag == 1:
        texto = fuente.render("Has probado a mover en la posicion " + str(hint_move) + " ?", True, white)
        pantalla.blit(texto, [0, 235])
    pygame.display.flip()
    if mode != 1 and player == 'O':
        move = games.alphabeta_search(state, game, d=difficult, cutoff_test=None,
                                      eval_fn=heuristic.compute_utility(state))
        state = game.make_move(move, state)
        grid[move[0]][move[1]] = 2
        cpu_log = "La CPU ha movido en la posicion" + str(move)
        player = 'X'
    if game.terminal_test(state):
        print "Final de la partida"
        break

    reloj.tick(20)

pygame.quit()
