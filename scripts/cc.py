from PIL import Image, ImageDraw, ImageFont, ImageFilter

def draw_gradient(im, color1, color2):
    draw = ImageDraw.Draw(im)
    width, height = im.size
    
    for x in range(width):
        r = int(color1[0] + (color2[0] - color1[0]) * x / width)
        g = int(color1[1] + (color2[1] - color1[1]) * x / width)
        b = int(color1[2] + (color2[2] - color1[2]) * x / width)
        draw.line([(x, 0), (x, height)], (r, g, b))

def draw_rounded_rectangle(self: ImageDraw, xy, corner_radius, fill=None, outline=None):
    """Draw a rounded rectangle.
    Taken from a stackoverflow post somehwere"""
    upper_left_point = xy[0]
    bottom_right_point = xy[1]

    self.rectangle([(upper_left_point[0], upper_left_point[1] + corner_radius), (bottom_right_point[0], bottom_right_point[1] - corner_radius)], fill=fill, outline=outline)
    self.rectangle([(upper_left_point[0] + corner_radius, upper_left_point[1]), (bottom_right_point[0] - corner_radius, bottom_right_point[1])], fill=fill, outline=outline)
    self.pieslice([upper_left_point, (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)], 180, 270, fill=fill, outline=outline)
    self.pieslice([(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2), bottom_right_point], 0, 90, fill=fill, outline=outline)
    self.pieslice([(upper_left_point[0], bottom_right_point[1] - corner_radius * 2), (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])], 90, 180, fill=fill, outline=outline)
    self.pieslice([(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]), (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)], 270, 360, fill=fill, outline=outline)

def create_image(card_num, card_name, expiry):
    cc = Image.new("RGBA", (754, 430), (255, 255, 255, 0))
    draw = ImageDraw.Draw(cc)

    chip = Image.open("scripts/cc-data/chip.png")
    chip = chip.resize((int(chip.width // 4), int(chip.height // 4)))

    mastercard = Image.open("scripts/cc-data/mastercard.png")
    mastercard = mastercard.resize((int(mastercard.width // 20), int(mastercard.height // 20)))

    ghost = Image.open("scripts/cc-data/ghost.png")
    ghost = ghost.resize((int(ghost.width // 13), int(ghost.height // 13)))

    mask = Image.open("scripts/cc-data/mask.png").convert("RGBA")
    watermark = Image.open("scripts/cc-data/watermark.png").convert("RGBA")

    large_font = ImageFont.truetype("scripts/cc-data/font.ttf", 65)
    small_font = ImageFont.truetype("scripts/cc-data/font.ttf", 35)
    watermark_font = ImageFont.truetype("scripts/cc-data/watermark.ttf", 35)

    background = Image.new("RGBA", (754, 430), (0, 0, 0, 0))
    draw_gradient(background, (61, 61, 61), (44, 44, 44))
    # draw_gradient(background, (106, 67, 153), (153, 67, 130))
    background.paste(watermark, (0, 0), watermark)
    background = Image.composite(background, cc, mask)
    cc.paste(background, (0, 0))

    cc.paste(chip, (80, int(cc.height / 2) - int(chip.height / 2) - 45), chip)
    # cc.paste(wireless, (80 + 130, int(cc.height / 2) - int(chip.height / 2) - 45 + 8), wireless)
    cc.paste(mastercard, (cc.width - mastercard.width - 20, cc.height - mastercard.height - 20), mastercard)
    draw.text((cc.width - mastercard.width + 35, cc.height - mastercard.height - 60), "DEBIT", (0, 0, 0), font=ImageFont.truetype("scripts/cc-data/watermark.ttf", 25), stroke_fill=(255, 255, 255), stroke_width=2)
    
    draw.text((int(cc.width / 2) - int(large_font.getlength(card_num) / 2) + 1, cc.height / 2 + 5 + 1), card_num, (0, 0, 0), font=large_font)
    draw.text((int(cc.width / 2) - int(large_font.getlength(card_num) / 2) - 1, cc.height / 2 + 5 - 1), card_num, (165, 165, 165), font=large_font)
    draw.text((int(cc.width / 2) - int(large_font.getlength(card_num) / 2), cc.height / 2 + 5), card_num, (255, 255, 255), font=large_font)
    
    draw.text((81, cc.height - 80 + 1), card_name.upper(), (0, 0, 0), font=small_font)
    draw.text((80 - 1, cc.height - 80 - 1), card_name.upper(), (165, 165, 165), font=small_font)
    draw.text((80, cc.height - 80), card_name.upper(), (255, 255, 255), font=small_font)

    draw.text((cc.width // 2 - small_font.getlength(expiry), cc.height - 120), "GOOD\nTHRU", (0, 0, 0), font=ImageFont.truetype("scripts/cc-data/watermark.ttf", 12), stroke_fill=(255, 255, 255), stroke_width=1)

    draw.text((cc.width // 2 + 1 - 30, cc.height - 120 + 1), expiry, (0, 0, 0), font=small_font)
    draw.text((cc.width // 2 - 1 - 30, cc.height - 120 - 1), expiry, (165, 165, 165), font=small_font)
    draw.text((cc.width // 2 - 30, cc.height - 120), expiry, (255, 255, 255), font=small_font)

    # cc.paste(ghost, (80, 40), ghost)
    # draw.text((80 + 45, 35), "Ghost Banking Inc", (255, 255, 255), font=watermark_font)

    cc.save("cc.png")
    return "cc.png"

@ghost.command(name="ccgen", description="Gen a fake credit card", usage="<user>", aliases=["creditcardgen"])
async def ccgen(ctx, user: discord.User = None):
    cfg = config.Config()

    if user is None:
        user = ctx.author

    new_user = requests.get(f"https://discord.com/api/users/{user.id}", headers={"Authorization": cfg.get("token")}).json()

    user_id = random.randint(1000, 9999) if str(user.id) == "0" else str(user.id)
    user_id = [user_id[i:i+4] for i in range(0, len(user_id), 4)]
    user_id.pop()
    user_id[0] = str(random.randint(50, 55)) + str(user_id[0][2:])
    card_num = " ".join(user_id)
    card_name = new_user["username"]
    expiry = str(random.randint(1, 12)) + "/" + str(random.randint(21, 30))

    await ctx.send(file=discord.File(create_image(card_num, card_name, expiry)))
    os.remove("cc.png")