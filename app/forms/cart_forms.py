from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, TextField, FileField,\
                    SelectField, IntegerField, Form, FormField, FieldList
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo, Optional


class AddItemToCart(Form):
    item_id = IntegerField(validators=[DataRequired()])
    quantity = IntegerField(validators=[DataRequired()])


class AddToCart(FlaskForm):
    cart_item = FormField(AddItemToCart)


class UpdateCartForm(FlaskForm):
    cart_items = FieldList(FormField(UpdateItemQuantityForm), min_entries=1)