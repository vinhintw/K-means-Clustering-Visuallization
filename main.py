try:
    import pygame, tkinter.filedialog, sys
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    from tkinter import messagebox
    from random import randint
    from skimage import io
    import math, numpy
    import webbrowser
    import warnings
    import time


    AUTHOR = "Vinh in Taiwan"
    version = "1.00.02"
    display_width = 1200
    display_height = 700
    screen = pygame.display.set_mode((display_width, display_height))
    pygame_icon = pygame.image.load('assets/label.png')
    pygame.display.set_icon(pygame_icon)

    pygame.display.set_caption("Learning K-means Algorithm")
    clock = pygame.time.Clock()

    #SETUP COLOR
    BLACK = (0,0,0)
    BACKGROUND_PANEL = (249, 255, 230)
    BACKGROUND_MENU = (131,134,132)
    WHITE = (255,255,255)

    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (147, 153, 35)
    PURPLE = (255,0,255)
    SKY = (0,255,255)
    ORANGE = (255,125,25)
    GRAPE = (100,25,125)
    GRASS = (55,155,65)

    COLORS = [RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]
    #SETUP FPS
    FPS = 120


    # Render text
    def create_text_render(string, color):
        font = pygame.font.SysFont('sans', 40)
        return font.render(string, True, color)

    # Create rect button
    def create_rect(color, pos):
        return pygame.draw.rect(screen, color, pos)

    def data_visualization():
        # Algorithm
        def distance(p1,p2):
            return math.sqrt((p1[0]-p2[0]) * (p1[0]-p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

        def print_points(points):
            vector_list = numpy.array(points)
            return vector_list

        # Set variable
        K = 0
        error = 0
        iteration = 0
        points = []
        clusters = []
        labels = []
        changed = True
        check_algorithm_button = False

        # Set font and text
        font = pygame.font.SysFont('sans', 40)
        font_small = pygame.font.SysFont('sans', 20)
        text_plus = create_text_render("+", WHITE)
        text_minus = create_text_render("-", WHITE)
        text_run = create_text_render("Run", WHITE)
        text_random = create_text_render("Random", WHITE)
        text_algorithm = create_text_render("Algorithm", WHITE)
        text_reset = create_text_render("Reset", WHITE)
        text_back = create_text_render("Back", WHITE)

        #Load logo
        icon = pygame.image.load('assets/mcuicon.png')
        # scale logo
        scale_percent = 20
        icon_width = int(icon.get_width() * scale_percent / 100)
        icon_height = int(icon.get_height() * scale_percent / 100)
        icon = pygame.transform.scale(icon, (icon_width, icon_height))
        icon = icon.convert()

        while True:
            # Set FPS game
            clock.tick(FPS)
            screen.fill(WHITE)
            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Draw interface #

            # Draw panel
            create_rect(BLACK, (50,50,700,500))
            create_rect(BACKGROUND_PANEL, (55,55,690,490))

            # Header
            text_visualization_header = font.render("Visualization: K-means Algorithm", True, BLACK)
            screen.blit(text_visualization_header, (350,600))

            #draw number of points
            text_error = create_text_render("Number of points = " + str(int(len(points))), BLACK)
            screen.blit(text_error, (825,50))

            # K value
            text_k = font.render("K = " + str(K), True, BLACK)
            screen.blit(text_k, (825,100))

            #draw error
            text_error = font.render("Error = " + str(int(error)), True, BLACK)
            screen.blit(text_error, (999,100))

            # Draw Iteration
            if changed == False:
                if check_algorithm_button == True:
                    text_iteration = font.render("Iteration: " + str(1), True, BLACK)
                    screen.blit(text_iteration, (825,150))
                    text_converge = font.render("Converged!", True, BLACK)
                    screen.blit(text_converge, (999,150))
                else:
                    # Draw Iteration
                    text_iteration = font.render("Iteration: " + str(iteration-1), True, BLACK)
                    screen.blit(text_iteration, (825,150))
            # Update Iteration
            if changed != False:
                # Draw Iteration
                text_iteration = font.render("Iteration: " + str(iteration), True, BLACK)
                screen.blit(text_iteration, (825,150))

            # Draw Converged message
            if changed == False:
                text_converge = font.render("Converged!", True, BLACK)
                screen.blit(text_converge, (999,150))

            # Draw MCU icon
            screen.blit(icon, (275, 590))

            # Draw Menu Option
            create_rect(BACKGROUND_MENU, (805,240,365,300))

            # Draw Menu option background
            text_error = font_small.render("Menu Options", True, WHITE)
            screen.blit(text_error, (930,240))

            # K button +
            create_rect(BLACK, (830,275,50,50))
            screen.blit(text_plus, (845,275))

            # K button -
            create_rect(BLACK, (930,275,50,50))
            screen.blit(text_minus, (950,275))

            # run button
            create_rect(BLACK, (830,375,150,50))
            screen.blit(text_run, (875,375))

            # random button
            create_rect(BLACK, (1000,275,150,50))
            screen.blit(text_random, (1010,275))

            # Reset button
            create_rect(BLACK, (1000,375,150,50))
            screen.blit(text_reset, (1030,375))

            # Back button
            create_rect(BLACK, (1000,475,150,50))
            screen.blit(text_back, (1040,475))

            # Algorithm button
            create_rect(BLACK, (830,475,150,50))
            screen.blit(text_algorithm, (830,475))

            # Show FPS
            fps = str(int(clock.get_fps()))
            font_fps = pygame.font.SysFont('sans', 14)
            fps_text = font_fps.render('FPS: '+fps, True, BLACK)
            screen.blit(fps_text, (1, 1))

            # Draw mouse position when mouse is in panel
            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                text_mouse = font_small.render("(" + str(mouse_x - 50) + "," + str(mouse_y - 50) + ")",True, BLACK)
                screen.blit(text_mouse, (mouse_x + 10, mouse_y))

            # End draw interface #

            # Draw cluster
            for i in range(len(clusters)):
                pygame.draw.circle(screen,COLORS[i], (int(clusters[i][0]) + 50, int(clusters[i][1]) + 50), 10)

            # Draw point
            for i in range(len(points)):
                pygame.draw.circle(screen,BLACK, (points[i][0] + 50, points[i][1] + 50), 5)

                if labels == []:
                    pygame.draw.circle(screen,WHITE, (points[i][0] + 50, points[i][1] + 50), 4)
                else:
                    pygame.draw.circle(screen,COLORS[labels[i]], (points[i][0] + 50, points[i][1] + 50), 4)

            # Calculate error
            error = 0
            if clusters != [] and labels != []:
                for i in range(len(points)):
                    error += distance(points[i], clusters[labels[i]])

            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check mouse when clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print(str(mouse_x),str(mouse_y))
                    # Create point on panel
                    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                        labels = []
                        iteration = 0
                        changed = True
                        check_algorithm_button = False
                        point = [mouse_x -50, mouse_y-50]
                        points.append(point)
                        #print(print_points(points))

                    # Change K button +
                    if 830 < mouse_x < 880 and 275 < mouse_y < 325:
                        if K < 8:
                            K += 1
                            #print("Press K +")

                    # Change K button -
                    if 930 < mouse_x < 980 and 275 < mouse_y < 325:
                        if K > 0:
                            K -= 1
                            #print("Press K -")

                    # Run button
                    if 830 < mouse_x < 980 and 375 < mouse_y < 425:
                        # Clear labels when pressed run button
                        labels = []
                        check_algorithm_button = False

                        # Update iteration when var is not None
                        if changed and K != 0 and points != [] and clusters != []:
                            iteration += 1


                        # Skip when cluster is None
                        if clusters == []:
                            continue

                        # Assign points to closet clusters
                        for p in points:
                            distances_to_cluster = []
                            for c in clusters:
                                dis = distance(p,c)
                                distances_to_cluster.append(dis)

                            min_distance = min(distances_to_cluster)
                            label = distances_to_cluster.index(min_distance)
                            labels.append(label)

                        # Update clusters
                        for i in range(K):
                            sum_x = 0
                            sum_y = 0
                            count = 0
                            for j in range(len(points)):
                                if labels[j] == i:
                                    sum_x += points[j][0]
                                    sum_y += points[j][1]
                                    count += 1

                            # Avoid divide by 0
                            if count != 0:
                                new_cluster_x = sum_x/count
                                new_cluster_y = sum_y/count
                                try:
                                    if numpy.all(clusters[i] != [new_cluster_x, new_cluster_y]):
                                        clusters[i] = [new_cluster_x, new_cluster_y]
                                        # Set check variable to True if cluster_positions changed
                                        changed = True

                                    else:
                                        changed = False

                                except:
                                    iteration = 0
                                    print('Erorr')

                        #print("Run pressed")

                        # Check Algorithm converges
                        if changed == False:
                            print('Converged')

                    # Random button
                    if 1000 < mouse_x < 1150 and 275 < mouse_y < 325:
                        labels = []
                        clusters = []
                        iteration = 0
                        changed = True
                        check_algorithm_button = False
                        for i in range(K):
                            random_point = [randint(0,700), randint(0,500)]
                            clusters.append(random_point)
                        if K != 0:
                            print("Random pressed")

                    # Reset button
                    if 1000 < mouse_x < 1150 and 375 < mouse_y < 425:
                        try:
                            K = 0
                            error = 0
                            sub_error = 0.1
                            iteration = 0
                            points = []
                            clusters = []
                            labels = []
                            changed = True
                            check_algorithm_button == False
                            print("Reset pressed")
                        except:
                            pass

                    # Algorithm
                    if 830 < mouse_x < 980 and 475 < mouse_y < 525:
                        try:
                            # turn off DeprecationWarning
                            warnings.filterwarnings("ignore", category=DeprecationWarning)
                            iteration = 2
                            changed = False
                            check_algorithm_button = True
                            if K == 0:
                                print("K could not be equal 0!")
                            if(points==[]):
                                print("You not yet create points!")
                            elif  K > len(points):
                                print("Point should be more than K!")

                            kmeans = KMeans(n_clusters=K, n_init=10).fit(points)
                            labels = kmeans.predict(points)
                            clusters = kmeans.cluster_centers_
                            print('Converged')
                        except:
                            changed = True
                            check_algorithm_button = False
                            iteration = 0
                            print("Error")

                    if 1000 < mouse_x < 1150 and 475 < mouse_y < 525:
                        check_algorithm_button == False
                        print("Main menu pressed")
                        main_menu()



            pygame.display.update()

    def application():
        # Open file
        def prompt_file():
            """Create a Tk file dialog and cleanup when finished"""
            top = tkinter.Tk()
            top.withdraw()  # hide window
            file_name = tkinter.filedialog.askopenfilename(parent=top)
            top.destroy()
            return file_name

        # Take image name
        def image_name(string):
            format1 = "\\"
            format2 = "/"
            format_image = ["jpg", "png"]
            if format1 in string:
                path_parts = string.split("\\")
                fileName= path_parts[-1]
                if not any(ext in fileName for ext in format_image):
                    raise ValueError("Your Input Must Be Is \".png\" or \".jpg\" Image")

            elif format2 in string:
                path_parts = string.split("/")
                fileName= path_parts[-1]
                if not any(ext in fileName for ext in format_image):
                    raise ValueError("Your Input Must Be Is \".png\" or \".jpg\" Image")

            return fileName

        # Run K-means Algorithm and save image, load image to screen
        def kmeans_run_image(file, cluster):
            try:
                print('Reading in image...please wait...')
                img = io.imread(file)
                #height, width, channels = img.shape
                width = img.shape[0]
                height = img.shape[1]
                img = io.imread(file)
                try:
                    channels = img.shape[2]
                except:
                    print('This is gray image!')

                print('Reading in image sucessfully!')
                print('...Running K means...')
                print("image info:", img.shape)

                # modelling
                for i in range(1, 11):
                    print('Compressing...'+ str(i)+'/10...', end='\r')
                    time.sleep(0.15)
                try:
                    # print(channels)
                    img = img.reshape(width*height,channels)
                    # print(img[0])
                except:
                    img = img.reshape(width*height, 1)
                    # print(img[0])
                    # img = img.reshape(2,-1)
                    # print(img[0])

                kMeans = KMeans(n_clusters = cluster, n_init=4)
                kMeans.fit(img)
                print('Almost done.\r')

                # getting centers and labels
                centers = numpy.asarray(kMeans.cluster_centers_, dtype=numpy.uint8)
                labels = numpy.asarray(kMeans.labels_, dtype = numpy.uint8)
                labels = numpy.reshape(labels, (width, height))
                # print(labels[0])
                #print(kMeans.cluster_centers_)

                try:
                    img2 = numpy.zeros((width,height,channels), dtype=numpy.uint8)
                except:
                    img2 = numpy.zeros((width,height), dtype=numpy.uint8)

                #index = 0
                for i in range(width):
                    for j in range(height):
                        # Assigning every pixel the RGBA color of its label's center
                        label_of_pixel = labels[i, j]
                        try:
                            img2[i, j, :] = centers[label_of_pixel, :]
                        except:
                            img2[i][j] = centers[label_of_pixel]
                        #    index += 1
                        #print(label_of_pixel)

                # Save
                io.imsave(file.split('.')[0] + '_'+str(cluster)+'_color.png', img2)
                newImage = file.split('.')[0] + '_'+str(cluster)+'_color.png'
                print('Image has been compressed sucessfully!')
                print('Image has been saved in: '+newImage)
                info = [newImage, ]
                return newImage
            except:
                return False

        # Draw message output
        def message_output():
            messagebox.showinfo("Message"," Compresess Successfully!")
            return True

        def visualize_show(file):
            img = plt.imread(file)
            fig = plt.figure(image_name(file))
            plt.imshow(img)
            plt.show()

            #im = Image.fromarray(img2)
        # Set font
        font_small = pygame.font.SysFont('sans', 20)

        # Set color
        color_inactive = BLACK
        color_active = RED
        color1 = color_inactive
        color2 = color_inactive

        # Set condition variable
        active_cluster = False
        active_img = False
        active_comfirm_cluster = False
        active_load_image_1 = False
        active_load_image_2 = False
        active_kmeans_button = False
        active_show_image = False

        # Set variable
        cluster = ''
        f = ''
        new_f = ''
        formats = ["png", "jpg"]

        #Load logo
        icon = pygame.image.load('assets/mcuicon.png')

        # scale logo
        scale_percent = 20
        icon_width = int(icon.get_width() * scale_percent / 100)
        icon_height = int(icon.get_height() * scale_percent / 100)
        icon = pygame.transform.scale(icon, (icon_width, icon_height))
        icon = icon.convert()
        #icon2 = pygame.transform.scale(icon2, (icon_width, icon_height))

        #Loop game
        while True:
            # Set FPS game
            clock.tick(FPS)

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Draw background color
            screen.fill(WHITE)

            # Draw interface

            # Draw MCU icon
            screen.blit(icon, (550, 35))

            # Name_Header
            text_application_header = font_small.render("Application: Image Compression", True, BLACK)
            screen.blit(text_application_header, (470,5))

            # Draw text enter file
            text_enter_file = font_small.render("Select image file here:", True, BLACK)
            screen.blit(text_enter_file, (100,30))

            # Draw input image box
            input_img_button = pygame.Rect(280, 25, 50, 30)
            pygame.draw.rect(screen, color2, input_img_button, 2)

            # Draw back button
            text_back = create_text_render("Back", WHITE)
            create_rect(BLACK, (1000,20,150,50))
            screen.blit(text_back, (1040,25))

            # Load image 1 to screen when active_load_image_1 is True
            if active_load_image_1:
                try:
                    img = pygame.image.load(f)
                    img = pygame.transform.scale(img, (420, 594))
                    img = img.convert()
                    screen.blit(img, (40, 88))
                except:
                    active_img = False
                    active_kmeans_button = False

            # Draw confirm file name
            if active_img:
                # Draw text confirm file
                text_confirm_file = font_small.render("Confirm file: " + str(image_name(f)), True, BLACK )
                screen.blit(text_confirm_file, (100, 53))

                # Draw cluster text input
                text_enter_cluster = font_small.render("cluster(enter number):", True, BLACK)
                screen.blit(text_enter_cluster, (720, 25))

                # Draw cluster input box
                input_cluster_box = pygame.Rect(900, 25, 50, 30)

                # Draw confirm cluster
                if active_comfirm_cluster:
                    if cluster != 0:
                        text_confirm_cluster = font_small.render("Confirm cluster: "+ cluster, True, BLACK)
                        screen.blit(text_confirm_cluster, (720, 53))

                        # chance text color if mouse in k-means button
                        if 490 <= mouse_x <= 590 and 300 <= mouse_y <= 350:
                            text_kmeans_run = create_text_render("K-Means", BLUE)
                        elif 570 <= mouse_x <= 660 and 270 <= mouse_y <= 380:
                            text_kmeans_run = create_text_render("K-Means", BLUE)
                        else:
                            text_kmeans_run = create_text_render("K-Means", BLACK)
                        # Draw K-means run buton
                        triangle_points = [(570, 270), (570, 380), (660, 320)]
                        pygame.draw.polygon(screen, BACKGROUND_MENU, triangle_points)
                        create_rect(BACKGROUND_MENU, (490,300,100,50))
                        screen.blit(text_kmeans_run, (495,300))


                        # Load compressed image
                        if active_kmeans_button:
                            try:
                                img3 = pygame.image.load(new_f)
                                img3 = pygame.transform.scale(img3, (421, 594))
                                img3 = img3.convert()
                                screen.blit(img3, (690, 88))
                                active_load_image_2 = True
                                if active_show_image :
                                    # chance text color if mouse in k-means button
                                    if 500 <= mouse_x <= 620 and 400 <= mouse_y <= 430:
                                        text_show = font_small.render("Visualize Show", True, BLUE)
                                    else:
                                        text_show = font_small.render("Visualize Show", True, BLACK)
                                    # Draw show visualize button
                                    create_rect(BACKGROUND_MENU, (500,400,120,30))
                                    screen.blit(text_show, (502,405))

                            except:
                                active_load_image_2 = False

                # Render the current text.
                txt_surface = font_small.render(cluster, True, BLACK)
                # Blit the text.
                screen.blit(txt_surface, (input_cluster_box.x+5, input_cluster_box.y+5))
                # Blit the input_box rect.
                pygame.draw.rect(screen, color1, input_cluster_box, 2)

            # Show FPS
            fps = str(int(clock.get_fps()))
            font_fps = pygame.font.SysFont('sans', 14)
            fps_text = font_fps.render('FPS: '+fps, True, BLACK)
            screen.blit(fps_text, (1, 1))

            # End draw interface

            # Event in application menu
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check mouse when clicked
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # When active_comfirm_cluster is True
                    if active_comfirm_cluster:

                        # Run if kmeans button is pressed #1
                        if 490 <= mouse_x <= 590 and 300 <= mouse_y <= 350:
                            progress_text = font_small.render(f"COMPRESSING", True, BLACK)
                            # Draw progress text on the screen
                            screen.blit(progress_text, (500, 210))
                            # Update the screen
                            pygame.display.flip()
                            print("Kmeans button pressed")
                            new_f = ''
                            new_f = kmeans_run_image(f, int(cluster))
                            if new_f != False:
                                active_kmeans_button = True
                                # Draw "Successfully" message
                                active_show_image = message_output()
                            else:
                                print('Erorr')

                        # Run if kmeans button is pressed #2
                        elif 570 <= mouse_x <= 660 and 270 <= mouse_y <= 380:
                            progress_text = font_small.render(f"COMPRESSING", True, BLACK)
                            # Draw progress text on the screen
                            screen.blit(progress_text, (500, 210))
                            # Update the screen
                            pygame.display.flip()
                            print("Kmeans pressed")
                            new_f = ''
                            new_f = kmeans_run_image(f, int(cluster))
                            if new_f != False:
                                active_kmeans_button = True
                                # Draw "Successfully" message
                                active_show_image = message_output()
                            else:
                                print('Erorr')

                        # When active_show_image is True
                        if active_show_image:
                            # Click on show_image button
                            if 500 <= mouse_x <= 620 and 400 <= mouse_y <= 430:
                                visualize_show(new_f)

                    # When Back button is pressed
                    if 1000 < mouse_x < 1150 and  20 < mouse_y < 70:
                        print("Main menu pressed")
                        main_menu()

                    # When choosed imput image
                    if input_img_button.collidepoint(event.pos):
                        active_img = True
                        color2 = color_active
                        color1 = color_inactive

                        try:
                            f = prompt_file()
                            print(f)
                            active_load_image_1 = True
                            print("image info:", io.imread(f).shape)

                            if image_name(f) == None:
                                pass

                        except:
                            active_img = False
                            print("Your Input Must Be Is \".png\" or \".jpg\" Image")

                    # Change Color box
                    elif active_img:
                        # If the user clicked on the input_box rect.
                        if input_cluster_box.collidepoint(event.pos):
                            # Toggle the active variable.
                            active_cluster = True
                            color1 = color_active
                            color2 = color_inactive

                        else:
                            active_cluster = False
                            # Change the current color of the input box.
                            color1 = color_inactive
                            color2 = color_inactive

                #check input image(drop iamge)
                if event.type == pygame.DROPFILE:
                    f = event.file
                    print(f)
                    print("image info:", io.imread(f).shape)
                    split_name = f.split(".")
                    ext = split_name[-1]
                    if ext in formats:
                        active_load_image_1 = True
                        active_img = True
                    else:
                        print("This file isn't an image, Your Input Must Be Is \".png\" or \".jpg\" Image")

                # input cluster
                if event.type == pygame.KEYDOWN:
                    # Truncate the cluter to maximum 16 and convert to integer

                    if active_cluster:
                        if event.key == pygame.K_RETURN:
                            try:
                                num = int(cluster)
                                if num == 0:
                                    raise ValueError("Input must be greater than 0")
                                # Truncate the cluter to maximum 16 and convert to integer
                                num = min(int(cluster), 16)
                                # Convert back to string and update text variable
                                # Convert back to string and update text variable
                                cluster = str(num)
                                print("cluster: "+cluster)
                                active_comfirm_cluster = True

                            except:
                                print("Input Erorr!")

                        # BACKSPACE button is presses
                        elif event.key == pygame.K_BACKSPACE:
                            cluster = cluster[:-1]
                            active_comfirm_cluster = False

                        else:
                            # Only allow input of digits (0-9)
                            if event.unicode.isdigit() and len(cluster) < 2:
                                cluster += event.unicode
                                active_comfirm_cluster = False

                    # Limit input to 2 digits and a maximum of 16
                    if len(cluster) > 2:
                        cluster = cluster[:2]

                    if cluster.isdigit() and int(cluster) > 16:
                        cluster = '16'

            #Upadte display
            pygame.display.update()

    #Load logo
    logo = pygame.image.load('assets/mculogo.png')
    # scale logo
    scale_percent = 70/100
    width = int(logo.get_width() * scale_percent )
    height = int(logo.get_height() * scale_percent)
    logo = pygame.transform.scale(logo, (width, height))
    logo = logo.convert()
    icon2 = pygame.image.load('assets/fish.png')
    icon2 = icon2.convert()
    flipped_image = pygame.transform.flip(icon2, True, False)

    def main_menu():
        link_color = (0, 0, 0)
        font_small = pygame.font.SysFont('sans', 18)
        # Draw text button
        text_visualization = create_text_render("Visualization", WHITE)
        text_application = create_text_render("Application", WHITE)
        app_info_text = font_small.render("Version: " + version +" Made by ", True, BLACK)

        while True:
            clock.tick(60)
            screen.fill(WHITE)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Draw interface

            # Render mcu logo
            screen.blit(logo, (display_width/4-100, 20))
            screen.blit(flipped_image, (display_width/2-350, 410))
            screen.blit(icon2, (700, 410))

            # Draw Visualization button
            create_rect(BLACK, (480,275,200,50))
            screen.blit(text_visualization, (490,275))

            # Draw application button
            create_rect(BLACK, (480,375,200,50))
            screen.blit(text_application, (497,375))

            # Draw app information and link
            screen.blit(app_info_text, (10,670))
            link = screen.blit(font_small.render(AUTHOR, True, link_color), (179, 670))


            #Evnet in main menu
            for event in pygame.event.get():
                #Quit game
                if event.type == pygame.QUIT:
                    print("Good Bye!")
                    pygame.quit()
                    sys.exit()

                # Check mouse when clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 480 < mouse_x < 680 and 275 < mouse_y < 325:
                        print("Data Visualization pressed")
                        data_visualization()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 480 < mouse_x < 680 and 375 < mouse_y < 425:
                        print("Application pressed")
                        application()
                    if link.collidepoint(event.pos):
                        webbrowser.open(r"https://vinhintw.info/")

            if link.collidepoint(pygame.mouse.get_pos()):
                link_color = (70, 29, 219)

            else:
                link_color = (0, 0, 0)

            # Update display
            pygame.display.update()


    if __name__== "__main__":
        pygame.init()
        main_menu()
except Exception as bug:
    print(bug)

input()