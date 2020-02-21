import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
  selector: 'app-articles',
  templateUrl: './articles.component.html',
  styleUrls: ['./articles.component.scss']
})

export class ArticlesComponent {

  @ViewChild('editions', { static: true }) editions: MatSidenav;

  selectedEdition: string;
  articles: [];

  onArticleSelected(selectedArticle) {
    // console.log(this.articles[0]['image']);
    this.editions.open();
  }

}
