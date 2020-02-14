import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleDetalisComponent } from './article-detalis.component';

describe('ArticleDetalisComponent', () => {
  let component: ArticleDetalisComponent;
  let fixture: ComponentFixture<ArticleDetalisComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArticleDetalisComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleDetalisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
