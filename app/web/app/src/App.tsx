import React, { useState } from 'react'
import './App.css'
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { InputTextarea } from 'primereact/inputtextarea';
import { Card } from 'primereact/card';
import SearchToolbar from './Toolbar/Toolbar';

interface ISearchResult {
    startIndex: number;
    endIndex: number;
    probability: number;
}

const THRESHOLD_PROBABILITY = 0.67;

function App() {
    const [originalText, setOriginalText] = useState('ты возьми корзину прежде чем набрать продукты');
    const [textToSearch, setTextToSearch] = useState('звонить');

    const [loadSearch, setLoadSearch] = useState(false);
    const [searchRequestDocument, setSearchRequestDocument] = useState('');
    const [searchRequestWord, setSearchRequestWord] = useState('');
    const [searchResult, setSearchResult] = useState<ISearchResult>(null);

    async function onSearch() {
        return;
        try {
            setLoadSearch(true);

            const document = originalText;
            const word = textToSearch;
            const response = await fetch('http://localhost:5151/search', {
                method: 'POST',
                body: JSON.stringify({
                    document,
                    word,
                }),
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            const searchResult: ISearchResult = await response.json();

            setSearchRequestDocument(document);
            setSearchRequestWord(word);
            setSearchResult(searchResult);
        } catch (ex) {
            onReset();
        } finally {
            setLoadSearch(false);
        }
    }

    function onReset() {
        setSearchRequestDocument('');
        setSearchRequestWord('');
        setSearchResult(null);
    }

    function updateFilter(data) {
        console.log('updateFilter', data);
    }

    const isEmptySearch =
        (searchResult?.startIndex === 0 && searchResult?.endIndex === 0)
        || searchResult?.probability < THRESHOLD_PROBABILITY;

    return (
        <main>
            <Card title="AI-агент поиска статей" className="main-description">
                <p className="m-0">
                    AI-агент для интеллектуального поиска и анализа статей технологических СМИ.
                    Способен находить статьи по запросу, генерировать краткое аннотированное резюме,
                    выводить ссылки на источники и предлагать пользователю
                    дополнительные функции поиска и анализа контента.
                </p>
            </Card>
            <SearchToolbar updateFilter={updateFilter}/>

            <div className='grid-input'>
                <div className="textarea">
                    <InputTextarea
                        value={originalText}
                        onChange={(e) => setOriginalText(e.target.value)}
                        rows={5}
                        placeholder={'Текст в котором ищем'}
                    />
                </div>
                <div className="controls">
                    <InputText
                        value={textToSearch}
                        onChange={(e) => setTextToSearch(e.target.value)}
                        placeholder={'Слова для поиска'}
                    />
                    <Button
                        label={loadSearch ? 'Поиск...' : 'Найти'}
                        onClick={onSearch}
                        disabled={!textToSearch || !originalText}
                    />
                    {Boolean(searchResult) && (
                        <Button
                            label="Сбросить"
                            severity="secondary"
                            onClick={onReset}
                        />
                    )}
                </div>
            </div>

            {(Boolean(searchResult) && !loadSearch) && (
                <div className='search-result'>
                    {isEmptySearch && (
                        <Card
                            title={`Вероятность совпадения ${Number(searchResult.probability * 100).toFixed(2)}%`}
                            subTitle={React.createElement('span', {className: 'error'}, searchRequestWord)}
                        >
                            <p className="m-0">
                                {searchRequestDocument}
                            </p>
                        </Card>
                    )}
                    {!isEmptySearch && (
                        <Card
                            title={`Вероятность совпадения ${Number(searchResult.probability * 100).toFixed(2)}%`}
                            subTitle={`Позиция ${searchResult.startIndex}-${searchResult.endIndex}`}
                        >
                            <p className="m-0">
                                {searchRequestDocument.slice(0, searchResult.startIndex)}
                                <span className='highlight'>{searchRequestDocument.slice(searchResult.startIndex, searchResult.endIndex + 1)}</span>
                                {searchRequestDocument.slice(searchResult.endIndex + 1)}
                            </p>
                        </Card>
                    )}
                </div>
            )}
        </main>
    );
}

export default App;
