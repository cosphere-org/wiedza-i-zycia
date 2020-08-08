import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

import { EditionsStore, ArticlesStore } from '@store';


@Component({
  selector: 'app-editions',
  templateUrl: './editions.component.html',
  styleUrls: ['./editions.component.scss']
})
export class EditionsComponent implements OnInit {

  @ViewChild('articles', { static: true }) articles: MatSidenav;

  selectedEdition: string;

  constructor(
    public store: EditionsStore,
    public articlesStore: ArticlesStore,
  ) {}

  ngOnInit() {
    this.store.bulkReadEditions();
  }

  onEditionSelected() {
    this.articles.open();
  }


}
