import { Component, Output, Input, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-editions-card',
  templateUrl: './editions-card.component.html',
  styleUrls: ['./editions-card.component.scss']
})

export class EditionsCardComponent  {

  @Input() edition;

  @Output() selected: EventEmitter<string> = new EventEmitter<string>();

}
