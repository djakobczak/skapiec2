from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, ValidationError

min_rep_choices = [(0, 'Brak'), (1, '1'), (2, '2'), (3, '3'), (4, '4')]


class MyFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Nieprawidłoy format danych'))


class ProductForm(FlaskForm):
    name = StringField('Nazwa produktu',
                        validators=[DataRequired(), Length(max=120)])
    min_price = MyFloatField('Cena minimalna (bez dostawy)', validators=[InputRequired(), NumberRange(min=0, message='Cena nie może być ujemna')],
                           )
    max_price = MyFloatField('Cena maksymalna (bez dostawy)',
                            validators=[InputRequired(), NumberRange(min=0, message='Cena nie może być ujemna')])
    count = IntegerField('Ilość',
                            validators=[InputRequired(), NumberRange(min=0, message='Ilość produktów musi być dodatnia')])
    min_rating = SelectField('Minimalna ocena sprzedawcy', validators=[], choices=min_rep_choices, coerce=int)
    nrates = IntegerField('Minimalna ilość opinii', validators=[InputRequired(), NumberRange(min=0, message='Ilość opinii nie może być ujemna')])
    submit_add = SubmitField('Dodaj')
    submit_search = SubmitField('Wyszukaj')

    def validate_max_price(self, max_price):
        min_price = self.min_price.data

        if max_price.data - min_price <= 0:
            raise ValidationError('Cena maksymalna musi być większa od ceny minimalnej')