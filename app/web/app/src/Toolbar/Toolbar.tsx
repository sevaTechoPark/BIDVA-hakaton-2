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
    onSearched: (data: ISearchResult | null) => void;
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

            const response = await fetch('http://localhost:5151/rag', {
                            method: 'POST',
                            body: JSON.stringify({
                                filter: {
                                    author: author ? author : undefined,
                                    start_date: dateRange[0],
                                    end_date: dateRange[1],
                                },
                                request_text: textToSearch,
                            }),
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        });
            const searchResult: {text: string; links: string[]} = await response.json();
            if (searchResult.text.includes('не найден')) {
                setHasSearchError(true);
                props.onSearched(null);
                return;
            }

            props.onSearched({
                annotation: searchResult.text,
                links: searchResult.links.map(link => {
                    return {
                        href: link,
                        label: link.replace(/^https?:\/\//, ''),
                    }
                }),
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
                    disabled={loadSearch || !textToSearch}
                />
                {hasSearchError && (
                    <span className="text-red">
                        Не найдены статьи на заданную тему
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