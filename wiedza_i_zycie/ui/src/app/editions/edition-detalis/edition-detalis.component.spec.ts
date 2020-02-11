import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditionDetalisComponent } from './edition-detalis.component';

describe('EditionDetalisComponent', () => {
  let component: EditionDetalisComponent;
  let fixture: ComponentFixture<EditionDetalisComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditionDetalisComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditionDetalisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
