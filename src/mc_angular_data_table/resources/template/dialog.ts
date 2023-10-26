import { Component, Inject } from "@angular/core";
import { {pascal_case}Service } from "../services/{kebab_case}.service";
import { {pascal_case} } from "./{pascal_case}";
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";

@Component({
    selector: 'dialog-{kebab_case}',
    templateUrl: 'dialog.html',
  })
  export class {pascal_case}Dialog {
  
    constructor(
      private {camel_case}Service: {pascal_case}Service,
      public dialogRef: MatDialogRef<{pascal_case}Dialog>,
      @Inject(MAT_DIALOG_DATA) public item: {pascal_case}) {}
  
    onCancel(): void {
      this.dialogRef.close();
    }
    onUpdate(): void {
      this.{camel_case}Service.update(this.item);
    }
  
  }