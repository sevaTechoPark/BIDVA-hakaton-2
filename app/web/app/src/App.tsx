import React, { useState } from 'react';
import './App.css';
import { Divider } from 'primereact/divider';
import { Card } from 'primereact/card';
import SearchToolbar, {ISearchResult} from './Toolbar/Toolbar';

function App() {
    const [searchResult, setSearchResult] = useState<ISearchResult>(null);

    function onSearched(data: ISearchResult) {
        setSearchResult(data);
    }

    return (
        <main>
            <Card title="AI-агент поиска статей">
                <span className="text-primary">
                    AI-агент для интеллектуального поиска и анализа статей технологических СМИ.
                    Способен находить статьи по запросу, генерировать краткое аннотированное резюме,
                    выводить ссылки на источники и предлагать пользователю
                    дополнительные функции поиска и анализа контента.
                </span>
            </Card>
            <SearchToolbar onSearched={onSearched}/>
            {Boolean(searchResult) && (
                <Card title="Аннотация">
                    <p className="annotation surface-0 border-round shadow-2 p-4 mb-4 text-justify">
                        {searchResult.annotation}
                    </p>
                    <Divider />
                    <div className="links">
                        {searchResult.links.map((item, i) => {
                            return (
                                <a key={i} href={item.href} className="p-text-secondary link" target="_blank" rel="noopener noreferrer">
                                    <i className="pi pi-share-alt"/>
                                    {item.label}
                                </a>
                            )
                        })}
                    </div>
                </Card>
            )}
        </main>
    );
}

export default App;
