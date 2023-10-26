import argparse
import json
from pathlib import Path
from importlib.resources import files

templates_dir = files("mc_angular_data_table") / "resources" / "template"

from model_codegen.models import Casing, Entity, Attribute, DataModel, from_json
from model_codegen.utils.stringmanipulation import (
    guess_plural,
    to_camel_case,
    to_kebab_case,
    to_pascal_case,
    to_snake_case
)


def generate(plugin_args):

    print(plugin_args)
    if len(plugin_args) != 2:
        raise ValueError("angular-data-table generate subcommand expects the following positional arguments `input`, `output_dir`.")
    input_path, output_path = plugin_args
    parent = Path(output_path)
    if parent.exists() and not parent.is_dir():
        raise ValueError(f"path '{parent}' is not a directory")
    

    input_model_path = Path(input_path)
    json_data = input_model_path.read_text()
    # print(json_data)
    model: DataModel = from_json(json_data)
    # print(model.entities)
    for entity in model.entities:
        wd = create_directory(entity, parent)
        print(generate_component(entity, wd))

def create_directory(entity, parent: Path):
    folder: Path = parent / entity.name
    folder.mkdir(exist_ok=True, parents=True)
    return folder


def generate_component(entity, wd: Path):
    ts_file_name = "component.ts"
    css_file_name = "styles.css"
    dialog_ts_file_name = "dialog.ts"
    ts_file = templates_dir / ts_file_name
    css_file = templates_dir / css_file_name
    dialog_ts_file = templates_dir / dialog_ts_file_name
    ts_text = replace_text_from_resource_file(entity, ts_file)
    dialog_ts_text = replace_text_from_resource_file(entity, dialog_ts_file)
    (wd / f"{to_kebab_case(entity.name)}.component.css").write_text(css_file.read_text())
    (wd /  f"{to_kebab_case(entity.name)}.component.ts").write_text(ts_text)
    (wd / dialog_ts_file_name).write_text(dialog_ts_text)
    dialog_html_text = build_dialog_html_text(entity)
    (wd / "dialog.html").write_text(dialog_html_text)
    component_html_text = build_component_html_text(entity)
    (wd / f"{to_kebab_case(entity.name)}.component.html").write_text(component_html_text)



def replace_text_from_resource_file(entity, ts_file):
    name = entity.name
    kebab_case = to_kebab_case(name)
    camel_case = to_camel_case(name)
    pascal_case = to_pascal_case(name)
    text = ts_file.read_text()
    return text \
        .replace("{kebab_case}", kebab_case) \
        .replace("{camel_case}", camel_case) \
        .replace("{pascal_case}", pascal_case)

   
def build_dialog_html_text(entity: Entity):
    text = """<div mat-dialog-content>
    <div class="flex flex-col">"""
    for attribute in entity.attributes:
        text += f"""
        <mat-form-field>
        <input
          matInput
          [(ngModel)]="item.{to_snake_case(attribute.name)}"
        />
      </mat-form-field>"""
    text += """</div>
  </div>
  <div mat-dialog-actions>
    <div class="flex flex-row grow w-1/2 justify-center">
      <button mat-button (click)="onCancel()">Cancel</button>
      <button
        mat-raised-button
        color="primary"
        (click)="onUpdate()"
        [mat-dialog-close]="item.when_created"
        cdkFocusInitial
      >
        Update
      </button>
    </div>
  </div>
    """
    return text

def build_component_html_text(entity):
    text = """<mat-spinner *ngIf="loading; else elseBlock"></mat-spinner>
<ng-template #elseBlock>
  <table
    mat-table
    [dataSource]="dataSource"
    matSort
    matSortDisableClear
    matSortActive="priority"
    matSortDirection="asc"
  >
    >"""
    for attribute in entity.attributes:
        text += f"""
    <ng-container matColumnDef="{attribute.name}">
      <th
        mat-header-cell
        *matHeaderCellDef
        mat-sort-header
        sortActionDescription="Sort by {attribute.name}"
      >
        {attribute.name}
      </th>
      <td mat-cell *matCellDef="let item">
        {{{{ item.{attribute.name} }}}}
      </td>
    </ng-container>
    """
    text += """
    <ng-container matColumnDef="edit">
      <th mat-header-cell *matHeaderCellDef>Edit</th>
      <td mat-cell *matCellDef="let item">
        <mat-icon (click)="editItem(item)">edit</mat-icon>
      </td>
    </ng-container>
    """
    text += """
    <ng-container matColumnDef="delete">
      <th mat-header-cell *matHeaderCellDef>Delete</th>
      <td mat-cell *matCellDef="let item">
        <mat-icon (click)="deleteItem(item)">delete</mat-icon>
      </td>
    </ng-container>
    """
    text += f"""
    <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
    <tr mat-row *matRowDef="let row; columns: displayedColumns"></tr>
  </table>
  <mat-paginator
    pageSize="5"
    [pageSizeOptions]="[5, 10, 20, 50]"
    showFirstLastButtons
    aria-label="Select page of {entity.name} items"
  >
  </mat-paginator>
</ng-template>
    """
    return text