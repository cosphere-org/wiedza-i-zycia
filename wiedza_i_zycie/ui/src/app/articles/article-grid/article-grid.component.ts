import { Component, EventEmitter, Output } from '@angular/core';
import { WizDataService } from 'src/app/wiz-data.service';

@Component({
  selector: 'app-article-grid',
  templateUrl: './article-grid.component.html',
  styleUrls: ['./article-grid.component.scss']
})
export class ArticleGridComponent {

  @Output() articleSelected: EventEmitter<string> = new EventEmitter<string>();

  articles;

  constructor(
    private wizDataService: WizDataService
  ) { }

  ngOnInit() {
    this.wizDataService.getWizJson().subscribe(editions => {
      
      this.articles = articles;
    });
  }

}
