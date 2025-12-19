import './Toolbar.css';
import React, {useState} from 'react'
import { InputText } from 'primereact/inputtext';
import { Toolbar } from 'primereact/toolbar';
import { Calendar } from 'primereact/calendar';
import { Fieldset } from 'primereact/fieldset';
import { FloatLabel } from 'primereact/floatlabel';
import {InputTextarea} from "primereact/inputtextarea";
import {Button} from "primereact/button";
import {ru} from './ruCalendar.ts';

type DateRange = {start?: Date; end?: Date;};

export interface ISearchResult {
    annotation: string;
    links: {
        href: string;
        label: string;
    }[];
}

interface IProps {
    onSearched: (data: ISearchResult) => void;
}

export default function SearchToolbar(props: IProps) {
    const [author, setAuthor] = useState('');
    const [subject, setSubject] = useState('');
    const [dateRange, setDateRange] = useState<DateRange>({});

    const [textToSearch, setTextToSearch] = useState('');
    const [loadSearch, setLoadSearch] = useState(false);
    const [hasSearchError, setHasSearchError] = useState(false);

    async function onSearch() {
        try {
            setLoadSearch(true);
            setHasSearchError(false);

            await new Promise(resolve => setTimeout(resolve, 2000));
            // const response = await fetch('http://localhost:5151/search', {
            //                 method: 'POST',
            //                 body: JSON.stringify({
            //                     document,
            //                     word,
            //                 }),
            //                 headers: {
            //                     'Content-Type': 'application/json',
            //                 },
            //             });
            //             const searchResult: ISearchResult = await response.json();
            props.onSearched({
                annotation: 'В современном мире информационных технологий стремительное развитие цифровых решений оказывает значительное влияние на все сферы жизни общества. Данная статья посвящена анализу ключевых тенденций в области IT, включая внедрение облачных вычислений, развитие искусственного интеллекта, автоматизацию бизнес-процессов и обеспечение кибербезопасности. Особое внимание уделяется вопросам интеграции новых технологий в существующую инфраструктуру предприятий, а также рассмотрению перспектив развития программного обеспечения с учетом современных требований рынка. В статье приводятся примеры успешных кейсов внедрения инновационных решений, обсуждаются основные вызовы, с которыми сталкиваются компании на пути цифровой трансформации, и предлагаются рекомендации по эффективному использованию IT-инструментов для повышения конкурентоспособности бизнеса. Кроме того, рассматривается роль специалистов в области информационных технологий в формировании цифровой экономики будущего.',
                links: [
                    { href: "https://habr.com/ru/articles/it", label: "Habr: IT-статьи" },
                    { href: "https://vc.ru/tech", label: "VC.ru: Технологии" },
                    { href: "https://www.cnews.ru/", label: "CNews: Новости IT" },
                    { href: "https://www.ixbt.com/", label: "iXBT: IT-обзоры" },
                    { href: "https://www.computerworld.com/", label: "Computerworld" },
                    { href: "https://www.techradar.com/", label: "TechRadar" },
                    { href: "https://www.wired.com/category/tech/", label: "Wired: Tech" }
                ],
            })
        } catch (ex) {
            setHasSearchError(true);
        } finally {
            setLoadSearch(false);
        }
    }

    const startContent = (
        <FloatLabel>
            <InputText
                id="author"
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
                placeholder={'Автор'}
            />
            <label htmlFor="author">{'Автор'}</label>
        </FloatLabel>
    );

    let calendarValue: [Date?, Date?] | null;
    if (dateRange.start && dateRange.end) {
        calendarValue = [dateRange.start, dateRange.end];
    } else if (dateRange.start) {
        calendarValue = [dateRange.start];
    } else {
        calendarValue = null;
    }

    const centerContent = (
        <FloatLabel>
            <Calendar<'range'>
                id="calendarValue"
                value={calendarValue}
                onChange={(e) => setDateRange({start: e.value[0], end: e.value[1]})}
                selectionMode="range"
                dateFormat="yy-mm-dd"
                maxDate={getMaxDate()}
                readOnlyInput
                hideOnRangeSelection
                placeholder={'Диапазон дат'}
            />
            <label htmlFor="calendarValue">{'Диапазон дат'}</label>
        </FloatLabel>


    );

    const endContent = (
        <FloatLabel>
            <InputText
                id="subject"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder={'Тематика'}
            />
            <label htmlFor="subject">{'Тематика'}</label>
        </FloatLabel>
    );

    return (
        <Fieldset legend="Фильтры" toggleable>
            <div className="filters-toolbar">
                <Toolbar start={startContent} center={centerContent} end={endContent}/>
                <FloatLabel>
                    <InputTextarea
                        id="textToSearch"
                        className="input-search"
                        value={textToSearch}
                        onChange={(e) => setTextToSearch(e.target.value)}
                        rows={2}
                        placeholder={'Фрагмент текста'}
                    />
                    <label htmlFor="textToSearch">{'Фрагмент текста'}</label>
                </FloatLabel>

                <Button
                    label={loadSearch ? 'Поиск...' : 'Мне повезёт'}
                    className="p-button-rounded"
                    onClick={onSearch}
                    disabled={loadSearch || (!textToSearch && (!author && !subject && !calendarValue))}
                />
                {hasSearchError && (
                    <span className="text-red">
                        Не повезло... Произошла ошибка
                    </span>
                )}
            </div>
        </Fieldset>

    );
}

function getMaxDate() {
    const nowDate = new Date();
    nowDate.setDate(nowDate.getDate() + 1);
    return nowDate;
}