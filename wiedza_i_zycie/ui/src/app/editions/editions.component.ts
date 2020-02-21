import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

import { EditionsStore } from '@store';


@Component({
  selector: 'app-editions',
  templateUrl: './editions.component.html',
  styleUrls: ['./editions.component.scss']
})
export class EditionsComponent implements OnInit {

  @ViewChild('editions', { static: true }) editions: MatSidenav;

  selectedEdition: string;

  articles: [];

  constructor(public store: EditionsStore) {}

  ngOnInit() {
    this.store.bulkReadEditions();
  }

  onEditionSelected(selectedEdition) {
    this.articles = selectedEdition['articles'];
    this.editions.open();
  }

}
