import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';


@Component({
  selector: 'app-editions',
  templateUrl: './editions.component.html',
  styleUrls: ['./editions.component.scss']
})
export class EditionsComponent {

  @ViewChild('editions', { static: true }) editions: MatSidenav;

  selectedEdition: string;
  articles: [];

  onEditionSelected(selectedEdition) {
    this.articles = selectedEdition['articles'];
    // console.log(this.articles[0]['image']);
    this.editions.open();
  }
}
