import { Component, Output, Input, EventEmitter } from '@angular/core';

import { ArticlesStore } from '@store';

@Component({
  selector: 'app-editions-card',
  templateUrl: './editions-card.component.html',
  styleUrls: ['./editions-card.component.scss']
})

export class EditionsCardComponent  {

  @Input() edition;

  @Output() editionSelected: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor(public store: ArticlesStore) {}

  onEditionSelected() {
    this.editionSelected.emit(true);
    this.store.bulkReadArticles(this.edition.articles);
  }
}
