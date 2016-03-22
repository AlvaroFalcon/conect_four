import pygame

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
LARGO = 20
ALTO = 20
MARGEN = 5

grid = []
for fila in range(7):
    grid.append([])
    for columna in range(6):
        grid[fila].append(0)

pygame.init()

pantalla = pygame.display.set_mode([700, 500])

pygame.display.set_caption("Connect 4")

done = False

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

    pantalla.fill(NEGRO)

    if intro_page == 1:
        texto = fuente.render("4 en raya", True, BLANCO)
        pantalla.blit(texto, [10, 10])

        texto = fuente.render("Realizado por:", True, ROJO)
        pantalla.blit(texto, [500, 400])

        texto = fuente.render("Alvaro Falcon Morales", True, BLANCO)
        pantalla.blit(texto, [400, 445])
        texto = fuente.render("Stefan Hautz", True, BLANCO)
        pantalla.blit(texto, [400, 470])

    if intro_page == 2:
        texto = fuente.render("Pulse m para cambiar la modalidad", True, BLANCO)
        pantalla.blit(texto, [10, 10])
        texto = fuente.render("Y de click para empezar!", True, BLANCO)
        pantalla.blit(texto, [10, 35])
        if mode == 1:
            texto = fuente.render("Modo: Multiplayer", True, BLANCO)
            pantalla.blit(texto, [10, 90])
        if mode == 2:
            texto = fuente.render("Modo: vs CPU", True, BLANCO)
            pantalla.blit(texto, [10, 90])
            texto = fuente.render("Dificultad: Facil", True, BLANCO)
            difficult = 1
            pantalla.blit(texto, [10, 120])
        if mode == 3:
            texto = fuente.render("Modo: vs CPU", True, BLANCO)
            pantalla.blit(texto, [10, 90])
            texto = fuente.render("Dificultad: Medio", True, BLANCO)
            difficult = 5
            pantalla.blit(texto, [10, 120])
        if mode == 4:
            texto = fuente.render("Modo: vs CPU", True, BLANCO)
            pantalla.blit(texto, [10, 90])
            texto = fuente.render("Dificultad: Dificil", True, BLANCO)
            difficult = 10
            pantalla.blit(texto, [10, 120])

    reloj.tick(20)

    pygame.display.flip()

while not done:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho = True
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            columna = pos[0] // (LARGO + MARGEN)
            fila = pos[1] // (ALTO + MARGEN)
            grid[fila][columna] = 1
            print("Click ", pos, "Coordenadas de la reticula: ", fila, columna)
    pantalla.fill(NEGRO)
    for fila in range(7):
        for columna in range(6):
            color = BLANCO
            if grid[fila][columna] == 1:
                color = VERDE
            pygame.draw.rect(pantalla,
                             color,
                             [(MARGEN + LARGO) * columna + MARGEN,
                              (MARGEN + ALTO) * fila + MARGEN,
                              LARGO,
                              ALTO])

    reloj.tick(20)

    pygame.display.flip()

pygame.quit()
