import solara
from typing import Type
from sqlmodel import SQLModel

from Solara_EditableTable import EditableSQLModelTable
from Solara_ModelForm import ModelForm
from Solara_Table import ModelTable
from setup_database import get_session, create_and_add

from models import Person
from SolaraTranscript_Page import TranscriptPage

@solara.component()
def Page():
    solara.Markdown("Testing the Transcription app features")

    TranscriptPage()


def main():
    Page()

if __name__ == "__main__":
    main()
