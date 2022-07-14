from subprocess import call
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

select_sex_keyboard = InlineKeyboardMarkup()
male_sex_button = InlineKeyboardButton("Мужской", callback_data="sex_M")
female_sex_button = InlineKeyboardButton("Женский", callback_data="sex_F")
select_sex_keyboard.add(male_sex_button, female_sex_button)

select_find_sex_keyboard = InlineKeyboardMarkup()
female_find_sex_button = InlineKeyboardButton("Девушки", callback_data="find_sex_F")
male_find_sex_button = InlineKeyboardButton("Парни", callback_data="find_sex_M")
all_find_sex_button = InlineKeyboardButton("Все", callback_data="find_sex_MF")
select_find_sex_keyboard.add(male_find_sex_button, female_find_sex_button, all_find_sex_button)


profile_settings_keyboard = InlineKeyboardMarkup(row_width=2)
profile_settings_name = InlineKeyboardButton("Поменять имя", callback_data="update_name")
profile_settings_age = InlineKeyboardButton("Поменять возраст", callback_data="update_age")
profile_settings_sex = InlineKeyboardButton("Изменить пол", callback_data="update_sex")
profile_settings_find_sex = InlineKeyboardButton("Изменить кого я хочу найти", callback_data="update_find_sex")
profile_settings_city = InlineKeyboardButton("Изменить город", callback_data="update_city")
profile_settings_photo_video = InlineKeyboardButton("Изменить фото/видео", callback_data="update_photo_video")
profile_settings_description = InlineKeyboardButton("Обновить описание", callback_data="update_description")
profile_settings_keyboard.add(profile_settings_name, profile_settings_age, profile_settings_sex, profile_settings_find_sex, profile_settings_photo_video, profile_settings_description, profile_settings_city)


cancel_button = InlineKeyboardButton("Отмена", callback_data="cancel")
update_sex_keyboard = InlineKeyboardMarkup(row_width=2).add(male_sex_button, female_sex_button, cancel_button)
update_find_sex_keyboard = InlineKeyboardMarkup().add(male_find_sex_button, female_find_sex_button, all_find_sex_button, cancel_button)

reaction_keyboard = InlineKeyboardMarkup()
reaction_like_button = InlineKeyboardButton("❤️", callback_data="reaction_like")
reaction_message_button = InlineKeyboardButton("💌", callback_data="reaction_message")
reaction_dislike_button = InlineKeyboardButton("👎", callback_data="reaction_dislike")
reaction_keyboard.add(reaction_like_button, reaction_message_button, reaction_dislike_button)
lite_reaction_keyboard = InlineKeyboardMarkup().add(reaction_like_button, reaction_dislike_button)

show_likes_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("Показать", callback_data="show_likes"))