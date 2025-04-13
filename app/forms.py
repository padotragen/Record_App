from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import app.dpmodule as dp


class SettingsForm(FlaskForm):
    collectionRefresh = SubmitField("Refresh Collection Data")
