import { Component, Output, EventEmitter, OnInit, ViewChild } from '@angular/core';
import { EditionsStore } from '@store';
import { MatProgressBar } from '@angular/material/progress-bar'
import { PageEvent, MatPaginator } from '@angular/material/paginator';

@Component({
  selector: 'app-editions-grid',
  templateUrl: './editions-grid.component.html',
  styleUrls: ['./editions-grid.component.scss']
})
export class EditionsGridComponent {

  start = 0;
  end = 10;
  length = 100;
  pageSize = 10;

  @Output() editionSelected: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor(public store: EditionsStore) {}


  ngOnInit() {
    // this.store.subsetEditions(this.start, this.end);
  }

  onPageChange(event){

    this.start = event.pageIndex * event.pageSize;
    this.end = this.start + event.pageSize;
    this.pageSize = event.pageSize;

    this.store.subsetEditions(this.start, this.end)
  }

}
