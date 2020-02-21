import { Component, Output, EventEmitter } from '@angular/core';
import { EditionsStore } from '@store';

@Component({
  selector: 'app-editions-grid',
  templateUrl: './editions-grid.component.html',
  styleUrls: ['./editions-grid.component.scss']
})
export class EditionsGridComponent {

  constructor(public store: EditionsStore) {}

}
