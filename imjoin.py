import os
import math
from PIL import Image


def join_images(main_image_folders, images_per_output, output_columns, img_width, img_height,
                line_thickness, line_color, name_output, format_output):
    if not os.path.isdir(main_image_folders):
        raise NotADirectoryError(f'{main_image_folders} not found.')

    for root, dirs, images in os.walk(main_image_folders):
        try:
            total_images_read = len(images)
            current_image_idx = 1
            num_output_images = math.ceil(total_images_read/images_per_output)
            images_used = []

            if total_images_read > 0:
                for output_image_idx in range(1, num_output_images + 1, 1):
                    # calculate the number of lines in the output image
                    num_lines_output_image = 0
                    if total_images_read > images_per_output:
                        if output_image_idx == num_output_images:
                            num_lines_output_image = int(math.ceil((total_images_read - current_image_idx + 1)
                                                                   / output_columns))
                        else:
                            num_lines_output_image = int(math.ceil(images_per_output/output_columns))
                    else:
                        num_lines_output_image = int(math.ceil(total_images_read/output_columns))

                    # used to iterate through  columns positions
                    lst_column_position = [x + 1 for x in range(output_columns)]
                    lst_column_position = lst_column_position * num_lines_output_image

                    # create background output image
                    output_image = Image.new(mode='RGB',
                                             size=(
                                                   (img_width*output_columns) + line_thickness*(output_columns - 1),
                                                   num_lines_output_image*img_height +
                                                   line_thickness*(num_lines_output_image - 1)
                                                  ),
                                             color=line_color)
                    pixel_map = output_image.load()

                    for image in images:
                        if image not in images_used:
                            # open image and resize
                            image_full_path = os.path.join(root, image)
                            img_open = Image.open(image_full_path)
                            image_resized = img_open.resize((img_width, img_height), Image.Resampling.LANCZOS)

                            # calculate the position of the current image in the output image
                            current_line = 0
                            current_column = lst_column_position[(current_image_idx - (output_image_idx - 1) *
                                                                 images_per_output) - 1]

                            if output_image_idx == 1:
                                current_line = int(math.ceil(current_image_idx/output_columns))
                            else:
                                current_line = math.ceil((current_image_idx - images_per_output*(output_image_idx - 1))
                                                        / output_columns)

                            # sweep the resized image and assign his value to the output image
                            for x in range(img_width):
                                for y in range(img_height):
                                    # getting the RGB pixel value.
                                    r, g, b = image_resized.getpixel((x, y))

                                    # setting the pixel value.
                                    pixel_map[search_x_value(x, img_width, current_column, line_thickness),
                                              search_y_value(y, img_height, current_line,  line_thickness)] = (r, g, b)

                            images_used.append(image)
                            current_image_idx += 1
                            img_open.close()
                            image_resized.close()

                            # exit if output image is ready
                            if (current_image_idx - 1) % images_per_output == 0:
                                break

                    # save output image in disk
                    full_path = os.path.join(root, name_output + str(output_image_idx) + format_output)
                    output_image.save(fp=full_path, quality=95)
                    # output_image.save(full_path)
                    output_image.close()
            else:
                print('No pictures selected!')
        except Exception as error:
            print('Error: ', error)


def search_x_value(x, img_width, current_column, line_thickness):
    # new column value
    new_x = 0

    if current_column == 1:  # First Column
        new_x = x
    else:
        new_x = x + (img_width + line_thickness)*(current_column - 1)

    return new_x


def search_y_value(y, img_height, current_line, line_thickness):
    # new line value
    new_y = 0

    if current_line == 1:  # First line
        new_y = y
    else:
        new_y = y + (img_height + line_thickness)*(current_line - 1)

    return new_y


if __name__ == '__main__':
    p_folder = r'D:\ProjetosPython\imagens'
    p_images_per_output = 8
    p_output_columns = 2
    p_img_width = 276
    p_img_height = 225
    p_line_thickness = 0
    p_line_color = '#E5CFB2'
    p_name_output = 'joinpic_'
    p_format_output = '.tiff'
    join_images(p_folder, p_images_per_output, p_output_columns, p_img_width, p_img_height,
                p_line_thickness, p_line_color, p_name_output, p_format_output)
