import uuid

try:
    from pages import LabelsPage
except ImportError:
    from .pages import LabelsPage


def unique_label_name(prefix="Label"):
    return f"{prefix} {uuid.uuid4().hex[:6]}"


def test_labels_table_loaded(authenticated_driver):
    labels = LabelsPage(authenticated_driver).open()

    labels.assert_headers("Name")


def test_create_label(authenticated_driver):
    labels = LabelsPage(authenticated_driver).open()
    name = unique_label_name()

    labels.create_label(name)

    assert labels.has_text(name)


def test_edit_label(authenticated_driver):
    labels = LabelsPage(authenticated_driver).open()
    name = unique_label_name()
    updated_name = unique_label_name("Updated Label")

    labels.create_label(name)
    labels.rename_label(name, updated_name)

    assert labels.has_text(updated_name)


def test_delete_label(authenticated_driver):
    labels = LabelsPage(authenticated_driver).open()
    name = unique_label_name()

    labels.create_label(name)
    labels.delete_label(name)

    assert not labels.has_text(name)
