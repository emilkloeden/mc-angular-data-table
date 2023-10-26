import {
    AfterViewInit,
    Component,
    OnInit,
    ViewChild
  } from '@angular/core';
  import { MatDialog } from '@angular/material/dialog';
  import { MatPaginator } from '@angular/material/paginator';
  import { MatSort } from '@angular/material/sort';
  import { MatTableDataSource } from '@angular/material/table';
  import { catchError, finalize, tap, throwError } from 'rxjs';
  import { {pascal_case} } from '../data-access/{pascal_case}';
  import { {pascal_case}Service } from '../data-access/{kebab_case}.service';
  import { {pascal_case}Dialog } from "./dialog";
  
  @Component({
    selector: 'app-{kebab_case}',
    templateUrl: './{kebab_case}.component.html',
    styleUrls: ['./{kebab_case}.component.css'],
  })
  export class {pascal_case}DataTableComponent
    implements OnInit, AfterViewInit
  {
    loading: boolean = false;
    items: {pascal_case}[] = [];
    item?: {pascal_case};
    displayedColumns: string[] = [{columns}];
  
    dataSource = new MatTableDataSource<{pascal_case}>(this.items);
  
    constructor(
      private {camel_case}Service: {pascal_case}Service,
      public dialog: MatDialog
    ) {}
  
    @ViewChild(MatSort) sort!: MatSort;
    @ViewChild(MatPaginator) paginator!: MatPaginator;
  
    ngAfterViewInit(): void {
      this.sort.sortChange.pipe(tap(() => this.loadItems())).subscribe();
    }
  
    ngOnInit() {
      this.loadItems();
    }
  
    loadItems() {
      this.loading = true;
      this.{camel_case}Service
        .findAll(this.sort?.direction ?? 'asc')
        .pipe(
          tap((items) => {
            this.items = items;
            this.dataSource.data = this.items;
            this.dataSource.sort = this.sort;
            this.dataSource.paginator = this.paginator;
          }),
          catchError((err) => {
            console.log('Error loading items', err);
            alert('Error loading items.');
            return throwError(err);
          }),
          finalize(() => {
            console.log('finalized');
            this.loading = false;
          })
        )
        .subscribe();
      this.loading = false;
      }

      editItem(item: {pascal_case}) {
        const dialogRef = this.dialog.open({pascal_case}Dialog, {
          maxWidth: '500px',
          width: '80%',
          data: item
        });
    
        dialogRef.afterClosed().subscribe(result => {
          this.item = item;
        });
      }

      deleteItem(item: {pascal_case}) {
        this.{camel_case}Service.delete(item);
      }
  }
  
  