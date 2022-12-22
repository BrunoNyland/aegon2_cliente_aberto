
name = 'name'
type = 'type'
x = 'x'
y = 'y'
width = 'width'
height = 'height'
children = 'children'
vertical_align = 'vertical_align'
horizontal_align = 'horizontal_align'

class types:
    window = 'window'
    button = 'button'
    radio_button = 'radio_button'
    toggle_button = 'toggle_button'
    mark = 'mark'
    image = 'image'
    expanded_image = 'expanded_image'
    ani_image = 'ani_image'
    slot = 'slot'
    grid_table = 'grid_table'
    text = 'text'
    editline = 'editline'
    box = 'box'
    bar = 'bar'
    line = 'line'
    slotbar = 'slotbar'
    gauge = 'gauge'
    listbox = 'listbox'
    listbox2 = 'listbox2'
    listboxex = 'listboxex'
    #################################################################################################################################
    ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ###
    #################################################################################################################################
    titlebar = 'titlebar'
    board = 'board'
    board_with_titlebar = 'board_with_titlebar'
    thinboard = 'thinboard'
    horizontalbar = 'horizontalbar'
    scrollbar = 'scrollbar'
    small_thin_scrollbar = 'small_thin_scrollbar'
    thin_scrollbar = 'thin_scrollbar'
    sliderbar = 'sliderbar'
    #################################################################################################################################
    ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ###
    #################################################################################################################################
    new_board = 'new_board'
    new_board_with_titlebar = 'new_board_with_titlebar'
    new_scrollbar = 'new_scrollbar'
    new_thin_scrollbar = 'new_thin_scrollbar'
    board_transparent = 'board_transparent'
    slider = 'slider'
    redbutton = 'redbutton'
    verticalseparator = 'verticalseparator'
    horizontalseparator = 'horizontalseparator'
    ballon = 'ballon'
    newradio_button = 'newradio_button'
    slot_elipse = 'slot_elipse'
    grid_table_elipse = 'grid_table_elipse'
    thinboardnew = 'thinboardnew'
    barwithbox = 'barwithbox'
    editboard = 'editboard'
    editboardfake = 'editboardfake'
    dropdown = 'dropdown'

class align:
    class vertical:
        center = 'center'
        bottom = 'bottom'
        top = 'top'
    class horizontal:
        center = 'center'
        right = 'right'
        left = 'left'

class default:
    x = 'x'
    y = 'y'
    vertical_align = 'vertical_align'
    horizontal_align = 'horizontal_align'
    all_align = 'all_align'
    hide = 'hide'
    istooltip = 'istooltip'
    children = 'children'

class window(default):
    width = 'width'
    height = 'height'

class button(default):
    width = 'width'
    height = 'height'
    set_type = 'set_type'
    default_image = 'default_image'
    over_image = 'over_image'
    down_image = 'down_image'
    disable_image = 'disable_image'
    text = 'text'
    text_height = 'text_height'
    text_color = 'text_color'
    tooltip_text = 'tooltip_text'
    tooltip_x = 'tooltip_x'
    tooltip_y = 'tooltip_y'

class radio_button(button):
    pass

class toggle_button(button):
    pass

class mark(default):
    pass

class image(default):
    image = 'image'
    alpha = 'alpha'

class expanded_image(image):
    width = 'width'
    height = 'height'
    x_origin = 'x_origin'
    y_origin = 'y_origin'
    x_scale = 'x_scale'
    y_scale = 'y_scale'
    rect = 'rect'
    mode = 'mode'
    rotation = 'rotation'
    percent = 'percent'

class ani_image(default):
    width = 'width'
    height = 'height'
    delay = 'delay'
    images = 'images'
    alpha = 'alpha'
    percent = 'percent'

class slot:
    x = 'x'
    y = 'y'
    width = 'width'
    height = 'height'
    image = 'image'
    image_r = 'image_r'
    image_g = 'image_g'
    image_b = 'image_b'
    image_a = 'image_a'

    slot = 'slot'
    class slots:
        index = 'index'
        x = 'x'
        y = 'y'
        width = 'width'
        height = 'height'

class grid_table:
    x_blank = 'x_blank'
    y_blank = 'y_blank'
    x = 'x'
    y = 'y'
    start_index = 'start_index'
    x_count = 'x_count'
    y_count = 'y_count'
    x_step = 'x_step'
    y_step = 'y_step'
    image = 'image'
    image_r = 'image_r'
    image_g = 'image_g'
    image_b = 'image_b'
    image_a = 'image_a'

    style = 'style'
    class styles:
        select = 'select'

class text(default):
    fontname = 'fontname'
    limit_width = 'limit_width'
    multi_line = 'multi_line'
    r = 'r'
    g = 'g'
    b = 'b'
    color = 'color'
    outline = 'outline'
    text = 'text'
    text_limited = 'text_limited'
    class align:
        horizontal = 'text_horizontal_align'
        vertical = 'text_vertical_align'

class editline(text):
    width = 'width'
    height = 'height'
    secret_flag = 'secret_flag'
    with_codepage = 'with_codepage'
    only_number = 'only_number'
    money_mode = 'money_mode'
    enable_codepage = 'enable_codepage'
    enable_ime = 'enable_ime'
    input_limit = 'input_limit'

class box(default):
    color = 'color'
    width = 'width'
    height = 'height'

class bar(default):
    color = 'color'
    width = 'width'
    height = 'height'

class line(default):
    color = 'color'
    width = 'width'
    height = 'height'

class slotbar(default):
    width = 'width'
    height = 'height'

class gauge(default):
    color = 'color'
    width = 'width'

class listbox(default):
    item_align = 'item_align'
    width = 'width'
    height = 'height'

class listbox2(listbox):
    row_count = 'row_count'

class listboxex(default):
    width = 'width'
    height = 'height'
    itemsize_x = 'itemsize_x'
    itemsize_y = 'itemsize_y'
    itemstep = 'itemstep'
    viewcount = 'viewcount'

#################################################################################################################################
### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ###
#################################################################################################################################
class titlebar(default):
    width = 'width'

class board(default):
    width = 'width'
    height = 'height'

class board_with_titlebar(board):
    title = 'title'

class thinboard(board):
    pass

class horizontalbar(default):
    width = 'width'

class scrollbar(default):
    size = 'size'
    midle_size = 'midle_size'

class small_thin_scrollbar(scrollbar):
    pass

class thin_scrollbar(scrollbar):
    pass

class sliderbar(default):
    pass

#################################################################################################################################
### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ###
#################################################################################################################################
class new_board(board):
    pass

class new_board_with_titlebar(board_with_titlebar):
    pass

class new_scrollbar(default):
    pass

class new_thin_scrollbar(scrollbar):
    pass

class board_transparent(board):
    pass

class slider(default):
    width = 'width'

class redbutton(default):
    width = 'width'
    text = 'text'
    text_height = 'text_height'
    tooltip_text = 'tooltip_text'
    tooltip_x = 'tooltip_x'
    tooltip_y = 'tooltip_y'

class verticalseparator(default):
    height = 'height'

class horizontalseparator(default):
    width = 'width'

class ballon(default):
    width = 'width'
    text = 'text'

class newradio_button(default):
    x = 'x'
    y = 'y'

class slot_elipse(slot):
    pass

class grid_table_elipse(grid_table):
    pass

class thinboardnew(default):
    width = 'width'
    height = 'height'

class barwithbox(default):
    width = 'width'
    height = 'height'
    color = 'color'
    box_color = 'box_color'
    flash_color = 'flash_color'


class editboard(default):
    width = 'width'
    height = 'height'
    color = 'color'
    box_color = 'box_color'
    flash_color = 'flash_color'
    fontsize = 'fontsize'
    fontname = 'fontname'
    text = 'text'
    text_color = 'text_color'
    text_center = 'text_center'
    infosize = 'infosize'
    info_color = 'info_color'
    info_font = 'info_font'
    info = 'info'
    secret_flag = 'secret_flag'
    only_number = 'only_number'
    input_limit = 'input_limit'

class editboardfake(default):
    width = 'width'
    height = 'height'
    color = 'color'
    box_color = 'box_color'
    flash_color = 'flash_color'
    fontsize = 'fontsize'
    fontname = 'fontname'
    text = 'text'
    text_color = 'text_color'
    text_center = 'text_center'

class dropdown(default):
    width = 'width'
    height = 'height'
    color = 'color'
    box_color = 'box_color'
    flash_color = 'flash_color'
    fontsize = 'fontsize'
    text = 'text'
    text_color = 'text_color'
    itens = 'itens'
    class item:
        text = 'text'
        value = 'value'





