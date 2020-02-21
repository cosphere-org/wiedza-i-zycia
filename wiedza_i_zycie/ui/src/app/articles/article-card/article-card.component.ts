import { Component, Output, Input, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-article-card',
  templateUrl: './article-card.component.html',
  styleUrls: ['./article-card.component.scss']
})
export class ArticleCardComponent{

  @Input() article;

  @Output() selected: EventEmitter<string> = new EventEmitter<string>();

}
