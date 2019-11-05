

# Responses table queries
class DBUtil:
def add_response_to_table(self, response,
def get_hero_id_by_response(self, response_url):
def get_link_for_response(self, response,

# Comments table queries
def add_comment_to_table(self, comment_id)
def delete_old_comment_ids(self):
def check_if_comment_exists(self, comment_id)


# heroes table queries
def add_hero_to_table(self, name,
def get_hero_id_from_table(self, name):
def get_hero_name(self, hero_id)
def get_hero_id_by_css(self, css)
def get_img_dir_by_id(self, hero_id)
def add_heroes_to_table(self):
def create_all_tables(self):
def drop_all_tables(self):
